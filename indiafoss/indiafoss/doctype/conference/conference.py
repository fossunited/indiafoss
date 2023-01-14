# Copyright (c) 2022, shridhar.p@zerodha..com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Conference(Document):
    pass


@frappe.whitelist(allow_guest=True)
def get_ticket_data(doc_name):
    st_price, gen_price, max_tickets, tickets_booked = frappe.get_value(
        "Conference",
        doc_name,
        [
            "student_ticket_price",
            "general_ticket_price",
            "max_tickets",
            "tickets_booked",
        ],
    )
    return {
        'student_ticket_price': st_price,
        'general_ticket_price': gen_price,
        'max_tickets': max_tickets,
        'tickets_booked': tickets_booked,
    }
