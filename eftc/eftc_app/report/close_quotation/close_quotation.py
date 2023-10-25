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
            "label": _("Close Quotation"),
            "fieldname": "count_quotation",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Quotation Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Quotation",
            "width": 200,
        },
    ]

    return columns

def get_data(filters=None):
    conditions = ""

    if filters.get('from_date') and filters.get('to_date'):
        conditions = "AND quotation.transaction_date BETWEEN {0} AND {1}".format(
            frappe.db.escape(filters.get('from_date')), 
            frappe.db.escape(filters.get('to_date'))
        )

    data = frappe.db.sql("""
        SELECT COUNT(name) as count_quotation, name
        FROM `tabQuotation` quotation
        WHERE quotation.docstatus = 1
          AND quotation.workflow_state = 'Approved By Customer'
          {}
        GROUP BY name
        LIMIT 10
    """.format(conditions), as_dict=True)

    return data


