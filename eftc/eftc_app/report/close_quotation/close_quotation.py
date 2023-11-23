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
    condition = ""
    if filters.get("from_date") and filters.get("to_date"):
        condition += " AND Date(quotation.creation) >= {0} AND Date(quotation.creation) <= {1}".format(
            frappe.db.escape(filters.get('from_date')), 
            frappe.db.escape(filters.get('to_date'))
            )

    if filters.get("company"):
        condition += " AND quotation.company = '{0}'".format(filters.get("company"))
    total_quotations = frappe.db.sql("""
        SELECT COUNT(name) as total_quotations
        FROM `tabQuotation` quotation
        WHERE quotation.docstatus = 1 {condition}
    """.format(condition = condition), as_dict=True)[0]['total_quotations']

    approved_quotations = frappe.db.sql("""
        SELECT COUNT(name) as approved_quotations
        FROM `tabQuotation` quotation
        WHERE quotation.docstatus = 1
          AND quotation.workflow_state = 'Approved By Customer' {condition}
    """.format(condition = condition), as_dict=True)[0]['approved_quotations']

    if total_quotations <= 0 and approved_quotations <= 0:
        total_quotation_percentage = 0
        approved_quotation_percentage = 0
    else:
        total_quotation_percentage = ((total_quotations - approved_quotations) / total_quotations) * 100
        approved_quotation_percentage = (approved_quotations / total_quotations) * 100
    data = [
        {'status': 'Other', 'percentage': total_quotation_percentage},
        {'status': 'Approved By Customer', 'percentage': approved_quotation_percentage}
    ]

    return data
