import frappe
from frappe.integrations.utils import make_get_request
from datetime import datetime, timedelta


def capture_pending_payments():
    # Marks payments paid at razorpay as captured in indiafoss
    time_after = datetime.now() - timedelta(minutes=55)
    time_before = datetime.now() - timedelta(minutes=5)
    all_orders = frappe.db.sql(
        """
        select name from `tabConference Payment`
        where payment_captured = 0 and creation >= %(time_after)s
        and creation < %(time_before)s
        and razorpay_order_id is not null
        order by creation asc
        """,
        values={
            "time_before": time_before.strftime("%Y-%m-%d %H:%M:%S"),
            "time_after": time_after.strftime("%Y-%m-%d %H:%M:%S"),
        },
        as_dict=1,
    )
    for order in all_orders:
        capture_payment(order["name"])


def capture_payment(ticket_id):
    doc = frappe.get_doc("Conference Payment", ticket_id)

    if doc.payment_captured:
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

    doc.save(ignore_permissions=True)
    frappe.db.commit()
