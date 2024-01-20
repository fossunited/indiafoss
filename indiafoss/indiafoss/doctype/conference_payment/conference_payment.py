# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


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
        db_gen_ticket_price, db_st_ticket_price,db_tshirt_price = frappe.db.get_value(
            "Conference",
            self.conference,
            ["general_ticket_price", "student_ticket_price", "tshirt_price"],
        )

        if self.general_ticket_price != db_gen_ticket_price:
            frappe.throw("price mismatch, please contact admin")

        if self.student_ticket_price != db_st_ticket_price:
            frappe.throw("price mismatch, please contact admin")

        expected_total = (
            int(self.student_tickets) * db_st_ticket_price
            + int(self.general_tickets) * db_gen_ticket_price
            + int(self.tshirt_count) * db_tshirt_price
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
