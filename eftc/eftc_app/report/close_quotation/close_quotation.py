# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt
import frappe
from frappe import _


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Percentage"),
            "fieldname": "percentage",
            "fieldtype": "Float",
            "width": 200,
        },
    ]

    return columns

def get_data(filters=None):
    total_quotations = frappe.db.sql("""
        SELECT COUNT(name) as total_quotations
        FROM `tabQuotation` quotation
    """, as_dict=True)[0]['total_quotations']

    approved_quotations = frappe.db.sql("""
        SELECT COUNT(name) as approved_quotations
        FROM `tabQuotation` quotation
        WHERE quotation.docstatus = 1
          AND quotation.workflow_state = 'Approved By Customer'
    """, as_dict=True)[0]['approved_quotations']

    data = [
        {'status': 'Other', 'percentage': ((total_quotations - approved_quotations) / total_quotations) * 100},
        {'status': 'Approved By Customer', 'percentage': (approved_quotations / total_quotations) * 100}
    ]

    return data
