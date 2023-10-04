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
 custom_sales_representative:function(frm) {
    frappe.call({
        method:"eftc.hook.quotation.get_mobile",
        args:{
            custom_sales_representative: frm.doc.custom_sales_representative
        },
        callback:function(r) {
            if (r.message) {
                frm.set_value("sales_representative_mobile_number",r.message)
                frm.refresh_field("sales_representative_mobile_number")
            }
            else {
                frappe.msgprint("Mobile Number Not found against the Sales Representative "+frm.doc.custom_sales_representative)
            }
        }
    });
 }
})