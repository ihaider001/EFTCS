import frappe
from erpnext import get_default_company
from frappe import _

def after_insert(doc , event):
    
    # Creating Traing Event for each item  on sales order creation
    for item in doc.items:
        training_event = frappe.get_doc({
            "doctype":"Training Creation",
            "course":item.item_name,
            "clientcustomer_name":doc.customer,
            "company":get_default_company(),
            "type":"Seminar",
        })
        training_event.insert(ignore_permissions=True,
                              ignore_mandatory=True)
        url = "<a href='{0}/app/training-creation/{1}'>{1}</a>".format(frappe.utils.get_url(),training_event.name)
        frappe.msgprint(
            _("Training Event Crated {0}".format(frappe.bold(url))),
            indicator="green",
            alert=1,
            )
        print(url,"JJ")
        # url = "<a href='{0}+/training-creation/{1}'>{1}</a>".format(frappe.utils.get_url(),doc.name)
        # frappe.msgprint(
        #     _("Training Event Crated {0}".format("<a href='{0}+/training-creation/{1}'>{2}</a>" )),
        #     indicator="green",
        #     alert=1,
        #     )