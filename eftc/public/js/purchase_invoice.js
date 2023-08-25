frappe.ui.form.on("Purchase Invoice", {
    refresh : function (frm) {
        frappe.call({
            method:"eftc.hook.quotation.set_qr_code_url",
            args:{
                doctype:"Purchase Invoice",
				docname:frm.doc.name,
				print_format : "Purchase Return",
				field_name:"qr_code_url"
            },
        })
   },
})