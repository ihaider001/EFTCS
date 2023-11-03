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
        frm.fields_dict['rounding_adjustment'].df.hidden = 1; 
        frm.fields_dict['rounded_total'].df.hidden = 1;
        frm.refresh_field("rounding_adjustment"); 
        frm.refresh_field("rounded_total");
   },
   customer_address : function (frm) {
    if (cur_frm.doc.customer_address){
     frappe.db.get_doc("Address",cur_frm.doc.customer_address).then(r=>{
      cur_frm.set_value("cr_number",r.cr_no)
      cur_frm.set_value("vat_number",r.vat_number_)
     })
      }
 },
 onload_post_render:function(frm) {
    console.log(frm.doc.party_name)
    if (frm.doc.quotation_to === "Lead" && frm.doc.docstatus === 0) {
        let customer_name = frappe.db.get_value("Customer",{"lead_name":frm.doc.party_name},"customer_name_in_arabic")
        .then((response) => {
                const customer_name = response.message.customer_name_in_arabic;
                frm.set_value("customer_name_in_arabic", customer_name);
                frm.set_value("customer_name", customer_name);
                frm.refresh_field("customer_name_in_arabic");
                if (!frm.doc.__islocal) {
                    frm.save()
                }
            })
            .catch((err) => {
                frappe.throw("Arabic name not set in customer.")
            });
    }
    else if (frm.doc.quotation_to === "Customer" && frm.doc.party_name && frm.doc.docstatus === 0) {
        let customer_name = frappe.db.get_value("Customer",frm.doc.party_name,"customer_name_in_arabic")
        .then((response) => {
            const customer_name = response.message.customer_name_in_arabic;
            frm.set_value("customer_name_in_arabic",customer_name);
            frm.refresh_field("customer_name_in_arabic");
            if (!frm.doc.__islocal) {
                frm.save()
            }
        })
        .catch((err) => {
            frappe.throw("Arabic name not set in customer.")
        })
    }
 },
 customer_name:function(frm) {
    if (frm.doc.quotation_to === "Customer" && frm.doc.party_name && frm.doc.docstatus === 0) {
        let customer_name = frappe.db.get_value("Customer",frm.doc.party_name,"customer_name_in_arabic")
        .then((response) => {
            const customer_name = response.message.customer_name_in_arabic;
            frm.set_value("customer_name_in_arabic",customer_name);
            frm.refresh_field("customer_name_in_arabic");
        })
        .catch((err) => {
            frappe.throw("Arabic name not set in customer.")
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