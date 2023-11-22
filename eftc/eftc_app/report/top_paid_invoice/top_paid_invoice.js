// Copyright (c) 2023, NestorBird and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Top Paid Invoice"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",  // Change "Company" to the actual doctype of your company
			"reqd": 1,  // Make it mandatory if needed
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "User",  // Change "Sales Person" to the actual doctype of your sales person
			"reqd": 0,  // Adjust as needed
			"default": frappe.session.user
		}
	]
};
