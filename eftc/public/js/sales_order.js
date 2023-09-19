frappe.ui.form.on("Sales Order", {
    delivery_date: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
		     d.delivery_date = frm.doc.delivery_date;
		});
		refresh_field("items");
	}
})
