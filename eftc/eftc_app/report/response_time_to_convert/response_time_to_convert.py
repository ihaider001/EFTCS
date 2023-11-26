# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data()
	return columns, data


def get_columns():
    columns = [
        {
            "label": _("Lead"),
            "fieldname": "lead_name",
            "fieldtype": "Link",
            "options":"Lead",
            "width": 200,
        },
        {
            "label": _("Lead Date "),
            "fieldname": "lead_date",
            "fieldtype": "Datetime",
            "width": 200,
        },
        {
            "label": _("Lead Days"),
            "fieldname": "lead_days",
            "fieldtype": "Int",
            "width": 200,
        },
        {
            "label": _("Opportunity"),
            "fieldname": "opportunity",
            "fieldtype": "Link",
            "options":"Opportunity",
            "width": 200,
        },
         {
            "label": _("Opportunity Date"),
            "fieldname": "opportunity_date",
            "fieldtype": "Datetime",
            "width": 200,
        },
        {
            "label": _("Quotation"),
            "fieldname": "quotation",
            "fieldtype": "Link",
            "options":"Quotation",
            "width": 200,
        },
        {
            "label": _("Quotation Date"),
            "fieldname": "quotation_date",
            "fieldtype": "Datetime",
            "width": 200,
        },
        {
            "label": _("Sales Order"),
            "fieldname": "sales_order",
            "fieldtype": "Link",
            "options":"Sales Order",
            "width": 200,
        },
        {
            "label": _("Sales Order Date "),
            "fieldname": "sales_order_date",
            "fieldtype": "Datetime",
            "width": 200,
        },
    ]

    return columns


def get_data():
      data = frappe.db.sql("""
								SELECT
									OP.name as "opportunity",
									LD.name as "lead_name",
									LD.creation as "lead_date",
									OP.creation as "opportunity_date",
									QT.name as "quotation",
									QT.creation as "quotation_date",
									DATEDIFF(OP.creation, LD.creation) as "lead_days",
									SOI.parent as sales_order,
									SOI.creation as sales_order_date
								FROM
									`tabOpportunity` OP
								JOIN
									`tabLead` LD ON LD.name = OP.party_name
									
								JOIN 
									`tabQuotation` QT ON LD.name = QT.party_name

								JOIN 
									`tabSales Order Item` SOI ON QT.name = SOI.prevdoc_docname
								WHERE
									OP.opportunity_from = "Lead"
						""",as_dict = 1)
      return data