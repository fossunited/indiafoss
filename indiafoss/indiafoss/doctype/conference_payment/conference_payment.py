# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class ConferencePayment(Document):
    def validate(self):

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
        if payment_status == "Authorized":
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
