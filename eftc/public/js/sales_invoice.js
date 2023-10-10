frappe.ui.form.on("Sales Invoice", {
  refresh:function(frm) {
        frm.fields_dict['rounding_adjustment'].df.hidden = 1; 
        frm.fields_dict['rounded_total'].df.hidden = 1;
        frm.refresh_field("rounding_adjustment"); 
        frm.refresh_field("rounded_total");
  },
    customer_address : function (frm) {
      if (cur_frm.doc.customer_address){
       frappe.db.get_doc("Address",cur_frm.doc.customer_address).then(r=>{
        cur_frm.set_value("custom_cr_number",r.cr_no)
        cur_frm.set_value("custom_vat_number_",r.vat_number_)
       })
        }
   },
})