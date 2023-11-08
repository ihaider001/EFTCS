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
    ]

    return columns

def get_data(filters = None):
    conditions = ""

    if filters.get('from_date') and filters.get('to_date'):
        conditions = "  AND transaction_date BETWEEN {0} AND {1}".format(
            frappe.db.escape(filters.get('from_date')), 
            frappe.db.escape(filters.get('to_date'))
        )
    reject_quote = frappe.db.sql("""Select count(*) as count_quotation from `tabQuotation` where workflow_state = 'Reject By Customer'""".format(conditions), as_dict=True)
    total_quote = frappe.db.sql("""Select count(*) as count_quotation from `tabQuotation` where workflow_state != 'Reject By Customer'""".format(conditions), as_dict=True)
    result_list = [
        {'workflow_state': 'Reject By Customer', 'count_quotation': reject_quote[0]['count_quotation']},
        {'workflow_state': 'Others', 'count_quotation': total_quote[0]['count_quotation']}
    ]
    return result_list



