"""Conference talk."""
# Copyright (c) 2022, shridhar.p@zerodha.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ConferenceTalks(Document):
    """Conference."""

    def before_insert(self):
        """Before insert validation."""
        if not is_accepting_proposals(self.conference):
            title = frappe.db.get_value("Conference", self.conference, "title")
            frappe.throw(
                f"<b>{title}</b> conference has stopped accepting proposals, for more details contact <b>Admin</b>"
            )


@frappe.whitelist(allow_guest=True)
def is_accepting_proposals(conference):
    """Check if conference is accept proposals or not"""
    start, end = frappe.db.get_value(
        "Conference", conference, ["cfp_start_date", "cfp_end_date"]
    )
    today = frappe.utils.data.today()
    if today >= str(start) and today <= str(end):
        return True
    else:
        return False
