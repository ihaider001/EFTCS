import frappe
from frappe import _
from eftc.eftc_app.report.sales_person_target_variance_based_on_item_group_for_chart.sales_person_target_variance_based_on_item_group_for_chart import get_sales_person




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
            "fieldname": "total_outstanding_amount",
            "fieldtype": "Float",
            "width": 200,
        }
    ]
    return columns


# def get_data(filters):
#     conditions = get_conditions(filters)
#     main = frappe.db.sql(f"""
#         SELECT
#             si.name AS invoice,
#             si.customer AS customer,
#             st.sales_person AS sales_person,
#             si.outstanding_amount AS total_outstanding_amount
#         FROM
#             `tabSales Invoice` AS si
#         JOIN
#             `tabSales Team` AS st ON si.name = st.parent
#         WHERE
#             si.docstatus = 1
#             AND si.outstanding_amount > 0
#             {conditions}
#         GROUP BY
#             si.customer, st.sales_person
#         ORDER BY
#             total_outstanding_amount DESC
#             LIMIT 5 
#     """, as_dict=True)
#     return main

def get_data(filters):
    conditions = get_conditions(filters)
    main = frappe.db.sql(f"""
        SELECT
            si.name AS invoice,
            si.customer AS customer,
            st.sales_person AS sales_person,
            si.outstanding_amount AS total_outstanding_amount
        FROM
            `tabSales Invoice` AS si
        JOIN
            `tabSales Team` AS st ON si.name = st.parent
        WHERE
            si.docstatus = 1
            AND si.outstanding_amount > 0
            {conditions}
        ORDER BY
            total_outstanding_amount DESC
            LIMIT 5 
    """, as_dict=True)
    return main

def get_conditions(filters):
    conditions = []
    if frappe.session.user == "Administrator":
        if filters['sales_person'] == "All":
            # conditions.append(f"AND st.is_group = 0 ")
            pass

        else:
            conditions.append(f"AND st.sales_person = {frappe.db.escape(filters['sales_person'])}")
    else :
        if filters.get("sales_person") == "All":
            
            sales_person = get_sales_person()
            for g in sales_person:
                print(g)
                if g != "All":
                    conditions.append(f"AND st.sales_person = {frappe.db.escape(g)}")
                    break
        else:
            conditions.append(f"AND st.sales_person = {frappe.db.escape(filters['sales_person'])}")


        
        
    if filters.get("company"):
        conditions.append(f"AND si.company = {frappe.db.escape(filters['company'])}")
    return " ".join(conditions)

