// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Target Variance Based On Item Group for chart"] = {
	"filters": [
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company")
		},
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: frappe.sys_defaults.fiscal_year
		},
		{
			fieldname: "doctype",
			label: __("Document Type"),
			fieldtype: "Select",
			options: "Sales Order\nDelivery Note\nSales Invoice",
			default: "Sales Order"
		},
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: [
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Half-Yearly", "label": __("Half-Yearly") },
				{ "value": "Yearly", "label": __("Yearly") }
			],
			default: "Monthly"
		},
		{
			fieldname: "target_on",
			label: __("Target On"),
			fieldtype: "Select",
			options: "Quantity\nAmount",
			default: "Quantity"
		},
		{
			fieldname: "sales_person",
			label: __("Sales Person"),
			fieldtype: "Select",
			options: get_sales_person(),
			default:"All"
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname.includes('variance')) {

			if (data[column.fieldname] < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			}
			else if (data[column.fieldname] > 0) {
				value = "<span style='color:green'>" + value + "</span>";
			}
		}

		return value;
	}



}


function get_sales_person(){
	var sales_per_list = []
	frappe.call({
	    method:"eftc.eftc_app.report.sales_person_target_variance_based_on_item_group_for_chart.sales_person_target_variance_based_on_item_group_for_chart.get_sales_person",
	    async:true,
	    callback:function(r) {
	        if (r.message) {
	        	r.message.forEach(function(e){
	        		sales_per_list.push(e)
	        		
	        	})
	        }
	    }
	});
	return sales_per_list
}