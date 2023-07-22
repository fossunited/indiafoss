# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document
from frappe.integrations.utils import make_get_request


class ConferencePayment(Document):

    def before_insert(self):
        self.validate_amounts()
        self.validate_ticket_count()

    def validate_ticket_count(self):
        # total tickets requesed for this payment
        tickets_requested = int(self.student_tickets) + int(self.general_tickets)

        if tickets_requested == 0:
            frappe.throw("Please select atleast one ticket to proceed.")

        max_tickets, tickets_booked = frappe.db.get_value(
            "Conference", self.conference, ["max_tickets", "tickets_booked"]
        )

        remaining_tickets = max_tickets - tickets_booked
        remaining_tickets = 0 if remaining_tickets < 0 else remaining_tickets

        if tickets_requested > remaining_tickets:
            frappe.throw(
                f"{remaining_tickets} tickets left for {self.conference} conference,\
                you are trying to book more."
            )

    def validate_amounts(self):
        db_gen_ticket_price, db_st_ticket_price = frappe.db.get_value(
            "Conference",
            self.conference,
            ["general_ticket_price", "student_ticket_price"],
        )

        if self.general_ticket_price != db_gen_ticket_price:
            frappe.throw("price mismatch, please contact admin")

        if self.student_ticket_price != db_st_ticket_price:
            frappe.throw("price mismatch, please contact admin")

        expected_total = (
            int(self.student_tickets) * db_st_ticket_price
            + int(self.general_tickets) * db_gen_ticket_price
        )

        if flt(expected_total, 2) != flt(self.total_amount, 2):
            frappe.throw("total mismatch, please contact admin")

    def on_payment_authorized(self, payment_status):
        # Run this when payment is authorized & not marked captured
        if payment_status == "Authorized" and self.payment_captured == 0:
            self.validate_amounts()

            self.payment_captured = 1

            # increase tickets booked count
            tickets_booked = frappe.db.get_value(
                "Conference", self.conference, "tickets_booked"
            )

            frappe.db.set_value(
                "Conference",
                self.conference,
                "tickets_booked",
                tickets_booked + self.student_tickets + self.general_tickets,
            )
            self.save(ignore_permissions=True)


def capture_payment(ticket_id):
    doc = frappe.get_doc('Conference Payment', ticket_id)

    if doc.payment_captured:
        return

    razorpay_settings = frappe.get_doc('Razorpay Keys')
    basic_auth = f'Basic {razorpay_settings.get_password("basic_auth")}'

    order = make_get_request(
        f'https://api.razorpay.com/v1/orders/{doc.razorpay_order_id}',
        headers={
            'Authorization': basic_auth,
            'Content-Type': 'application/json'
        }
    )

    doc.payment_captured = True if order['status'] == 'paid' else False

    if doc.payment_captured:
        if doc.total_amount != order['amount_paid'] / 100:
            frappe.throw(f"invalid amounts {doc.total_amount} {order['amount_paid'] / 100}")

        tickets_booked = int(frappe.db.get_value(
            "Conference", doc.conference, "tickets_booked"
        ))

        frappe.db.set_value(
            "Conference",
            doc.conference,
            "tickets_booked",
            tickets_booked + int(doc.student_tickets) + int(doc.general_tickets),
        )

    doc.save(ignore_permissions=True)
    frappe.db.commit()


def capture_pending_payments():
    # Marks payments paid at razorpay as captured in indiafoss
    all_orders = frappe.db.sql(
        """
        select name from `tabConference Payment`
        where payment_captured = 0 and creation >= (NOW() - INTERVAL 30 MINUTE)
        and creation < (NOW() - INTERVAL 5 MINUTE)
        and razorpay_order_id is not null
        order by creation asc
        """,
        as_dict=1
    )
    for order in all_orders:
        capture_payment(order["name"])
