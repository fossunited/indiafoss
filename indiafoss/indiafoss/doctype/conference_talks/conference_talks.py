"""Conference talk."""
# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ConferenceTalks(Document):
    """Conference."""

    def before_insert(self):
        """Before insert validation."""
        start, end, title = frappe.db.get_value(
            "Conference", self.conference, ["cfp_start_date", "cfp_end_date", "title"]
        )
        today = frappe.utils.data.today()
        if today >= str(start) and today <= str(end):
            pass
        else:
            frappe.throw(f"<b>{title}</b> has stopped accepting proposals, for more details contact <b>Admin</b>")
