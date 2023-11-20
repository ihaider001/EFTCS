// Copyright (c) 2023, NestorBird and contributors
// For license information, please see license.txt

frappe.ui.form.on('TS', {
	refresh: function(frm) {
		window.location.replace("/app/training-schedule/"+frm.doc.training_schedule);
	},
	onload: function(frm) {
		window.location.replace("/app/training-schedule/"+frm.doc.training_schedule);
	}
});
