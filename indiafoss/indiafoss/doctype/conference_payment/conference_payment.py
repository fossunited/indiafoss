# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ConferencePayment(Document):

    def on_payment_authorized(self, payment_status):
        if payment_status == "Authorized":
            self.payment_captured = 1
            self.save(ignore_permissions=True)
