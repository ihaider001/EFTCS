frappe.ui.form.on("Purchase Order", {
    refresh : function (frm) {
        frappe.call({
            method:"eftc.hook.quotation.set_qr_code_url",
            args:{
                doctype:"Purchase Order",
				docname:frm.doc.name,
				print_format : "Purchase Order",
				field_name:"qr_code_url"
            },
        })
   },
})