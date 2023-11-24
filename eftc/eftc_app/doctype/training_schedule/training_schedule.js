// Copyright (c) 2023, NestorBird and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Schedule', {
	validate:function(frm){
		for( var attendee in frm.doc.attendees){
			var cdn = frm.doc.attendees[attendee]["name"]
			frappe.model.set_value("Attendees Table", cdn, "course", frm.doc.course_name)
			
		}
	},
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
	after_save: function(frm) {

		frappe.call({
			method:"eftc.eftc_app.doctype.training_schedule.training_schedule.create_training_schedule_calender",
			args:{
				"data":frm.doc
			}
		})
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
	iqamaid_no:function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		var iqamaid_ = [];
		var dup_iqamaid_ = [];
		var current_iqamaid_no = d.iqamaid_no
	
		var cnt = 0;
		frm.doc.attendees.forEach(function(e){
			if(iqamaid_.includes(e["iqamaid_no"])){
				if(current_iqamaid_no == e["iqamaid_no"]){
					frappe.model.set_value(cdt, cdn, 'iqamaid_no', "")
				}
				if(e["iqamaid_no"] == ""){
					dup_iqamaid_.push(current_iqamaid_no);
				}else{
					dup_iqamaid_.push(e["iqamaid_no"]);
				}
				cnt += 1;
			}else{
				if(e["iqamaid_no"] != ""){
					iqamaid_.push(e["iqamaid_no"]);
				}
			}
		})
		
		if (cnt > 0){
			frappe.msgprint(__('Duplicate IQAMA/ID NO: '+dup_iqamaid_+' in Attendees Table'));
		}

	}
});
