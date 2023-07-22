import frappe
from frappe.integrations.utils import make_get_request


def capture_pending_payments():
    # Marks payments paid at razorpay as captured in indiafoss
    all_orders = frappe.db.sql(
        """
        select name from `tabConference Payment`
        where payment_captured = 0 and creation >= CONVERT_TZ(NOW(), '+00:00','+05:30') - INTERVAL 1 HOUR
        and creation < CONVERT_TZ(NOW(), '+00:00','+05:30') - INTERVAL 5 MINUTE
        and razorpay_order_id is not null
        order by creation asc
        """,
        as_dict=1,
    )
    for order in all_orders:
        try:
            capture_payment(order["name"])
        except Exception as e:
            frappe.log_error(e, "capture payment job Failed")


def capture_payment(ticket_id):
    doc = frappe.get_doc("Conference Payment", ticket_id)

    if doc.payment_captured:
        frappe.log_error(f"payment already captured {doc.name}", "capture payment job Failed")
        return

    razorpay_settings = frappe.get_doc("Razorpay Keys")
    basic_auth = f'Basic {razorpay_settings.get_password("basic_auth")}'

    order = make_get_request(
        f"https://api.razorpay.com/v1/orders/{doc.razorpay_order_id}",
        headers={"Authorization": basic_auth, "Content-Type": "application/json"},
    )

    doc.payment_captured = True if order["status"] == "paid" else False

    if doc.payment_captured:
        if doc.total_amount != order["amount_paid"] / 100:
            frappe.log_error(
                f"invalid amounts {doc.total_amount} {order['amount_paid'] / 100}",
                "capture payment job Failed",
            )
            frappe.throw(
                f"invalid amounts {doc.total_amount} {order['amount_paid'] / 100}"
            )

        tickets_booked = int(
            frappe.db.get_value("Conference", doc.conference, "tickets_booked")
        )

        frappe.db.set_value(
            "Conference",
            doc.conference,
            "tickets_booked",
            tickets_booked + int(doc.student_tickets) + int(doc.general_tickets),
        )

    doc.save()
    frappe.db.commit()
