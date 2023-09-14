frappe.ui.form.on("Quotation", {
    refresh : function (frm) {
        frappe.call({
            method:"eftc.hook.quotation.set_qr_code_url",
            args:{
                doctype:"Quotation",
				docname:frm.doc.name,
				print_format : "Quotation",
				field_name:"qr_code_url"
            },
        })
   },
   customer_address : function (frm) {
    if (cur_frm.doc.customer_address){
     frappe.db.get_doc("Address",cur_frm.doc.customer_address).then(r=>{
      cur_frm.set_value("cr_number",r.cr_no)
      cur_frm.set_value("vat_number",r.vat_number_)
     })
      }
 },
})