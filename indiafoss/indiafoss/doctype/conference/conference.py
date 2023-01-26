# Copyright (c) 2022, shridhar.p@zerodha..com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Conference(Document):
    pass


@frappe.whitelist(allow_guest=True)
def get_ticket_data(doc_name):
    exists = frappe.db.exists("Conference", doc_name)
    if not exists:
        return {
            'student_ticket_price': 0,
            'general_ticket_price': 0,
            'max_tickets': 0,
            'tickets_booked': 0,
        }

    st_price, gen_price, max_tickets, tickets_booked = frappe.get_value(
        "Conference",
        exists,
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
