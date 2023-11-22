# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",  
            "width": 200,
        },
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person",  
            "width": 200,
        },
        {
            "label": _("Amount"),
            "fieldname": "paid_amount",
            "fieldtype": "Float",
            "width": 200,
        }
    ]
    return columns

def get_data(filters):
    conditions = get_conditions(filters)
    main = frappe.db.sql(f"""
        SELECT
            si.name AS invoice,
            si.customer AS customer,
            st.sales_person AS sales_person,
            si.grand_total AS paid_amount
        FROM
            `tabSales Invoice` AS si
        JOIN
            `tabSales Team` AS st ON si.name = st.parent
        WHERE
            si.docstatus = 1
            AND si.status = 'Paid'
            {conditions}
        ORDER BY
            si.grand_total DESC
            LIMIT 5 
    """, as_dict=True)
    return main

def get_conditions(filters):
    conditions = []
    if filters.get("sales_person"):
        employee = frappe.db.get_value("Employee",{"user_id":filters['sales_person']},"name")
        sales_man = frappe.db.get_value("Sales Person",{"employee":employee},"name")
        if sales_man:
            conditions.append(f"AND st.sales_person = {frappe.db.escape(sales_man)}")
    if filters.get("company"):
        conditions.append(f"AND si.company = {frappe.db.escape(filters['company'])}")
    return " ".join(conditions)