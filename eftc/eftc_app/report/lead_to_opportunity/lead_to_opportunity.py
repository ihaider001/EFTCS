# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_column()
	data = get_data()
	return columns, data


def get_column():
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


def get_data():
	all_leads = frappe.db.sql("""Select status, name from `tabLead`""",as_dict = True)
	lost = frappe.db.sql("""SELECT COUNT(*) as num FROM `tabLead` WHERE status = 'Lost Quotation' OR status = 'Do Not Contact'""", as_dict=True)
	total_leads = len(all_leads)
	total_leads = total_leads - lost[0]['num']
	lead_count = len([lead for lead in all_leads if lead['status'] == 'Lead' and lead['status'] != 'Lost Quotation' and lead['status'] != 'Do Not Contact'])
	lead_percentage = (lead_count / total_leads) * 100
	other_count = total_leads - lead_count
	other_percentage = (other_count / total_leads) * 100
	result_list = [
        {'status': 'Lead', 'percentage': lead_percentage},
        {'status': 'Lead Converted', 'percentage': other_percentage}
    ]
	return result_list