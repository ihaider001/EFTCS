# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import json






class TrainingSchedule(Document):
    def on_submit(self):

        # Creating Training Schedule Feedback
        create_training_schedule_feedback(self)


        # Creating Certificate for every attendee on submit of Training schedule
        for attendee in self.attendees:
            year = int(attendee.get("validity"))
            days = year*365

            expiry_date = frappe.utils.add_days(attendee.get("issue_date"),days),
            attendee.expiry_date = expiry_date
            certificate =frappe.get_doc({
                "doctype":"Certificate",
                "attendee_name":attendee.get("attendee_name"),
                "course":attendee.get("course"),
                "iquama_no":attendee.get("iqamaid_no"),
                "issue_date":attendee.get("issue_date"),
                "upload_photo":attendee.get("upload_photo"),
                "sales_invoice":attendee.get("sales_invoice"),
                "training_schedule":self.get("name"),
                "expiry":expiry_date,
                "trainer_name":self.get("trainer_name"),
                "created_by": frappe.session.user
            }).insert(ignore_permissions = True)
            self.save(ignore_permissions = True)
            url = "<a href='{0}/app/certificate/{1}'>{2}</a>".format(frappe.utils.get_url(),certificate.name,certificate.attendee_name)
            frappe.msgprint(
                _("Certificate Created for {0}".format(frappe.bold(url))),
                indicator="green",
                alert=1,
                )
              


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def attendee_dropdown(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
    return frappe.db.sql("""Select
                         name ,
                         attendee_name
                         from `tabAttendee Register`
                         """
                        )

@frappe.whitelist()
def create_sales_invoice(values,docname):
    # Converting Selected Values into Json
    json_data = json.loads(values)

    # Training Schedule Details
    training_schedule = frappe.get_doc("Training Schedule", docname)

    # Sales Order Details
    sales_order_details = frappe.get_doc("Sales Order",training_schedule.sales_order)
    
    # Creating Sales Invoice 
    sales_invoice = frappe.new_doc("Sales Invoice")
    sales_invoice.customer = sales_order_details.customer
    sales_invoice.training_schedule = docname
    sales_invoice.append("items",{
        "item_code":training_schedule.course,
        "qty":len(json_data["undefined"]),
        "amount":len(json_data["undefined"]) * training_schedule.course_amount
    })
    for attendee in json_data["undefined"]:
        sales_invoice.append("attendee",{
            "attendee_name":attendee.get("attendee_name"),
            "course":attendee.get("course"),
            "issue_date":attendee.get("issue_date"),
            "validity":attendee.get("validity"),
            "iqamaid_no":attendee.get("iqamaid_no")
        })
    sales_invoice.save(ignore_permissions=1)
    url = "<a href='{0}/app/sales-invoice/{1}'>{1}</a>".format(frappe.utils.get_url(),sales_invoice.name)
    frappe.msgprint(
        _("Sales Invoice Created {0}".format(frappe.bold(url))),
        indicator="green",
        alert=1,
        )

    # Updating Training Schedule child table 
    for attendees in sales_invoice.attendee:
        for trainees in training_schedule.attendees:
            if attendees.iqamaid_no == trainees.iqamaid_no:
                trainees.sales_invoice = sales_invoice.name
    training_schedule.save()
    

def create_training_schedule_feedback(self):
    frappe.get_doc({
        "doctype":"Training Schedule Feedback",
        "employee":self.get("trainer"),
        "course":self.get("course"),
        "training_schedule":self.get("name")
        }).insert(ignore_permissions = True , ignore_mandatory = True)


