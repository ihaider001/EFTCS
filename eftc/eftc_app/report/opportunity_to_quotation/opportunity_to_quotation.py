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
	all_opportunity = frappe.db.sql("""Select status, name from `tabOpportunity`""",as_dict = True)
	lost = frappe.db.sql("""SELECT COUNT(*) as num FROM `tabOpportunity` WHERE status = 'Lost' OR status = 'Closed'""", as_dict=True)
	print(lost,"===")
	total_opportunity = len(all_opportunity)
	total_opportunity = total_opportunity - lost[0]['num']
	opportunity_count = len([opp for opp in all_opportunity if opp['status'] == 'Open' and opp['status'] != 'Lost' and opp['status'] != 'Closed'])
	opp_percentage = (opportunity_count / total_opportunity) * 100
	other_count = total_opportunity - opportunity_count
	other_percentage = (other_count / total_opportunity) * 100
	result_list = [
		{'status': 'Open', 'percentage': opp_percentage},
		{'status': 'Opportunity Converted', 'percentage': other_percentage}
	]
	return result_list