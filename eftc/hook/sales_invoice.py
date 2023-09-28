import frappe
from frappe.model.naming import make_autoname

def on_submit(doc,method):
    for attendee in doc.attendee:
        attendee_name = frappe.db.get_value("Attendees Table",{"parent":doc.training_schedule,"attendee_name":attendee.attendee_name},"name")
        frappe.db.set_value("Attendees Table", attendee_name,"sales_invoice", doc.name)
    training_event = frappe.get_doc("Training Schedule",doc.training_schedule)
    counter = 0
    for attendee in training_event.get("attendees"):
        if attendee.sales_invoice:
            counter+=1
    if len(training_event.get("attendees")) == counter:
        training_event.isbillled = 1
        training_event.save()
    


def autoname(doc,event):
    doc.so_naming_series= make_autoname(f"SO.-.####.")