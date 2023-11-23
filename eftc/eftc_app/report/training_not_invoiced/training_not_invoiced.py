import frappe

def execute(filters=None):
    columns = [
        {"label": "Training Schedule", "fieldname": "training_schedule", "fieldtype": "Link", "options": "Training Schedule"},
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
    ]

    data = get_training_schedule_statuses(filters)

    return columns, data

def get_conditions(filters):
    conditions = []
    if filters.get("sales_person"):
        employee = frappe.db.get_value("Employee", {"user_id": filters['sales_person']}, "name")
        sales_man = frappe.db.get_value("Sales Person", {"employee": employee}, "name")
        if sales_man:
            conditions.append(f"st.sales_person = {frappe.db.escape(sales_man)}")
    if filters.get("company"):
        conditions.append(f"so.company = {frappe.db.escape(filters['company'])}")
    
    # Join conditions with 'AND' only if there are conditions
    if conditions:
        return " AND ".join(conditions)
    else:
        return ""

def get_training_schedule_statuses(filters):
    conditions = get_conditions(filters)
    
    query = f"""
        SELECT
            ts.name AS training_schedule,
            so.name AS sales_order,
            CASE
                WHEN COUNT(DISTINCT at.sales_invoice) = 0 THEN 'Not Invoiced'
                WHEN SUM(CASE WHEN at.sales_invoice IS NOT NULL THEN 1 ELSE 0 END) < COUNT(DISTINCT at.attendee_name) THEN 'Partially Invoiced'
                ELSE ''
            END AS status
        FROM
            `tabTraining Schedule` AS ts
        LEFT JOIN
            `tabAttendees Table` AS at ON ts.name = at.parent
        LEFT JOIN
            `tabSales Order` AS so ON ts.sales_order = so.name
        LEFT JOIN
            `tabSales Team` AS st ON so.name = st.parent
        WHERE
            {conditions}
        GROUP BY
            ts.name
        HAVING
            status != ''
    """
    main = frappe.db.sql(query, as_dict=True)
    return main