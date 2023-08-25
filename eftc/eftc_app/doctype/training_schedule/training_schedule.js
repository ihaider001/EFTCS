// Copyright (c) 2023, NestorBird and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Schedule', {
	onload: function(frm) {
		frm.set_query('attendee', 'attendees', () => {
			return {
				query:"eftc.eftc_app.doctype.training_schedule.training_schedule.attendee_dropdown",
			}
		})
	
	},

	refresh:function(frm){
		if (!frm.doc.__islocal){
		frm.add_custom_button(__('Create Sales Invoice'), () =>
			frm.trigger("create_sales_invoice")
		);
		}
	},

	create_sales_invoice: function(frm) {
		let attendee_data = []
		for ( var attendee in frm.doc.attendees){
			if (!frm.doc.attendees[attendee]["sales_invoice"]){
				attendee_data.push(frm.doc.attendees[attendee])
			}
		}

		let dialog = new frappe.ui.Dialog({
			title: 'Create Sales Invoice',
			size: "large",
			fields: [
				{
					fieldtype: 'Table',
					cannot_add_rows: true,
					// in_place_edit: true,
					fields: [
						{ fieldname: 'attendee', fieldtype: 'Read Only', in_list_view: 1, label: 'Attendee',width:2 },
						{ fieldname: 'attendee_name', fieldtype: 'Read Only', in_list_view: 1, label: 'Attendee_name'},
						{ fieldname: 'iquama_no', fieldtype: 'Read Only', in_list_view: 1, label: 'IQUAMA NO'},
					],
					data:attendee_data
				}
			],
			primary_action_label: __('Create Invoice'),
			primary_action: (values) => {
				frappe.call({
					method:'eftc.eftc_app.doctype.training_schedule.training_schedule.create_sales_invoice',
					args:{'values':values,
						"docname":frm.doc.name}
					
				})
				dialog.hide();
				}
		});
		dialog.show();	
	}

	
});

frappe.ui.form.on('Attendees Table', {
	attendee:function(frm,cdt,cdn){
		frappe.model.set_value(cdt, cdn, 'course', cur_frm.doc.course)
		cur_frm.refresh_fields("course");
	}
});
