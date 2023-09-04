// Copyright (c) 2023, NestorBird and contributors
// For license information, please see license.txt

frappe.ui.form.on('Certificate', {
	before_save: function(frm) {
		frappe.call({
            method:"eftc.hook.quotation.set_qr_code_url",
            args:{
                doctype:"Certificate",
				docname:frm.doc.name,
				print_format : "Certificate",
				field_name:"qr_code_url"
            },
        })
	}
});
