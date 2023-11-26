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
            "label": _("Quotation Rejected"),
            "fieldname": "count_quotation",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Quotation status"),
            "fieldname": "workflow_state",
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
    conditions = ""

    if filters.get('from_date') and filters.get('to_date'):
        conditions += "AND transaction_date BETWEEN {0} AND {1}".format(
            frappe.db.escape(filters.get('from_date')), 
            frappe.db.escape(filters.get('to_date'))
        )
    
    if filters.get('company'):
        conditions += " AND Company = {0}".format(
            frappe.db.escape(filters.get('company')), 

        )

    reject_quote = frappe.db.sql("""
        SELECT COUNT(*) as count_quotation
        FROM `tabQuotation`
        WHERE workflow_state = 'Reject By Customer'
        {0}
    """.format(conditions), as_dict=True)[0]['count_quotation']

    total_quote = frappe.db.sql("""
        SELECT COUNT(*) as count_quotation
        FROM `tabQuotation`
        WHERE workflow_state != 'Reject By Customer'
        {0}
    """.format(conditions), as_dict=True)[0]['count_quotation']

    total_quotations_count = reject_quote + total_quote

    if total_quotations_count == 0:
        others_percentage = 0
        rejected_quote_percentage = 0
    else:
        others_percentage = (total_quote / total_quotations_count) * 100
        rejected_quote_percentage = (reject_quote / total_quotations_count) * 100
    data = [
        {'workflow_state': 'Others', 'count_quotation': total_quote, 'percentage': others_percentage},
        {'workflow_state': 'Reject By Customer', 'count_quotation': reject_quote, 'percentage': rejected_quote_percentage}
    ]

    return data
