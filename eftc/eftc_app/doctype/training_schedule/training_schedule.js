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
	iscompleted: function(frm) {
		frm.set_value("color","#29CD42")

	},

	refresh:function(frm){
		if (!frm.doc.__islocal)  {
				frm.add_custom_button(__('Create Sales Invoice'), () =>
				frm.trigger("create_sales_invoice")
		);
		if ( (frappe.user.has_role("Employee"))  && (!frappe.user.has_role("System Manager"))){
			frm.remove_custom_button('Create Sales Invoice');
			// Hiding Connections tab
			$(".form-links").hide();


		}
	}

	},

	before_save:function(frm){
		frm.set_value("total_participants" , frm.doc.attendees.length)
	},
	create_sales_invoice: function(frm) {
		let attendee_data = []
		for ( var attendee in frm.doc.attendees){
			if (!frm.doc.attendees[attendee]["sales_invoice"]){
				var dict = { "attendee_name":frm.doc.attendees[attendee]["attendee_name"],
							"iqamaid_no":frm.doc.attendees[attendee]["iqamaid_no"],
							"course":frm.doc.attendees[attendee]["course"],
							"issue_date":frm.doc.attendees[attendee]["issue_date"],
							// "validity":frm.doc.attendee[attendee]["validity"]
				  }
				attendee_data.push(dict)
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
						{ fieldname: 'attendee_name', fieldtype: 'Read Only', in_list_view: 1, label: 'Attendee_name'},
						{ fieldname: 'iqamaid_no', fieldtype: 'Read Only', in_list_view: 1, label: 'IQUAMA NO'},
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
	attendee_name:function(frm,cdt,cdn){
		frappe.db.get_doc("Item",cur_frm.doc.course).then(r=>{
		frappe.model.set_value(cdt, cdn, 'course', r.item_name)
		})
	}
});
