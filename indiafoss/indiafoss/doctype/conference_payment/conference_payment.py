# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ConferencePayment(Document):
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
                tickets_booked
                + self.student_tickets
                + self.general_tickets,
            )
            self.save(ignore_permissions=True)
