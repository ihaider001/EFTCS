frappe.ui.form.on("Sales Invoice", {
    customer_address : function (frm) {
      if (cur_frm.doc.customer_address){
       frappe.db.get_doc("Address",cur_frm.doc.customer_address).then(r=>{
        cur_frm.set_value("custom_cr_number",r.cr_no)
        cur_frm.set_value("custom_vat_number_",r.vat_number_)
       })
        }
   },
})