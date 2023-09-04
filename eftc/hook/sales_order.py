import frappe
from erpnext import get_default_company
from frappe import _

def on_submit(doc , event):
    
    # Creating Traing Event for each item  on sales order submittion
    for item in doc.items:
        training_event = frappe.get_doc({
            "doctype":"Training Schedule",
            "course":item.item_code,
            "clientcustomer_name":doc.customer,
            "company":get_default_company(),
            "type":"Seminar",
            "sales_order":doc.name        })
        training_event.insert(ignore_permissions=True,
                              ignore_mandatory=True)
        url = "<a href='{0}/app/training-schedule/{1}'>{1}</a>".format(frappe.utils.get_url(),training_event.name)
        frappe.msgprint(
            _("Training Event Created {0}".format(frappe.bold(url))),
            indicator="green",
            alert=1,
            )



