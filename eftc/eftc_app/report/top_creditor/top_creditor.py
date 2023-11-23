# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    conditions = get_conditions(filters)
    data = frappe.db.sql(f"""
        SELECT 
            si.customer AS Customer,
            SUM(si.grand_total) AS TotalSalesAmount
        FROM 
            `tabSales Invoice` AS si
        LEFT JOIN
            `tabSales Team` AS st ON si.name = st.parent
        WHERE 
            si.docstatus = 1
            {conditions}
        GROUP BY 
            si.customer
        ORDER BY 
            TotalSalesAmount DESC
        LIMIT 5
    """, as_dict=True)

    columns = [
        {"label": "Customer", "fieldname": "Customer", "fieldtype": "Link", "options": "Customer", "width": 120},
        {"label": "Total Sales Amount", "fieldname": "TotalSalesAmount", "fieldtype": "Currency", "options": "currency", "width": 150},
    ]

    return columns, data

def get_conditions(filters):
    conditions = []
    if filters.get("sales_person"):
        employee = frappe.db.get_value("Employee", {"user_id": filters['sales_person']}, "name")
        sales_man = frappe.db.get_value("Sales Person", {"employee": employee}, "name")
        if sales_man:
            conditions.append(f"AND st.sales_person = '{sales_man}'")
    if filters.get("company"):
        conditions.append(f"AND si.company = '{filters['company']}'")
    
    # Add more conditions as needed
    return " ".join(conditions)
