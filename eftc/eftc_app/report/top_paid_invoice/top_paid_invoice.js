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
};



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