frappe.ui.form.on("Sales Order", {
	refresh : function (frm) {     
		cur_frm.set_value("disable_rounded_total",1)  
		frm.set_df_property('disable_rounded_total', 'hidden',1); 
   },
    delivery_date: function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
		     d.delivery_date = frm.doc.delivery_date;
		});
		refresh_field("items");
	}
})
