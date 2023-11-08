# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	columns = [
        {
            "label": _("Lost Reason"),
            "fieldname": "lost_reason",
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
	data = frappe.db.sql("""Select lost_reason, parent from `tabOpportunity Lost Reason Detail`;""",as_dict=True)
	

    # Step 1: Get The Total
	total_entries = len(data)
	
    # Step 2: get The count of every lost_reason
	reason_count = {}
	for entry in data:
		lost_reason = entry["lost_reason"]
		if lost_reason in reason_count:
			reason_count[lost_reason] += 1
		else:
			reason_count[lost_reason] = 1
			
    # Step 3: Calculate percentage
	reason_percentage = {}
	for reason, count in reason_count.items():
		percentage = (count/total_entries) * 100
		reason_percentage[reason] = percentage
		

    # Step 5: Create a list of dictionaries with lost_reason and percentage

	result_list = [{'lost_reason': reason, 'percentage': percentage} for reason, percentage in reason_percentage.items()]
	print(result_list,"======")
	return result_list


	