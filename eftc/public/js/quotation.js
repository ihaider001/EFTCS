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
})