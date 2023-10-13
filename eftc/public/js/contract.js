frappe.ui.form.on("Contract", {
     party_name: function (frm) {
        if (frm.doc.party_type==="Customer" && frm.doc.party_name)
        {
            frappe.db.get_doc("Customer",frm.doc.party_name).then(r=>{
                if (r.customer_primary_address){
                    console.log("address",r.customer_primary_address)
                    frappe.db.get_doc("Address",r.customer_primary_address).then(result=>{
                        console.log("result",result.name)
                        frm.set_value("vat_number",result.vat_number_)
                        refresh_field("vat_number")
                        frm.set_value("cr_number",result.cr_no)
                        refresh_field("cr_number")
                    })
                }
            })
        }
    
    }})
