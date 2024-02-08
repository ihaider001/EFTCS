# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import json
from frappe.utils import get_url
import datetime






class TrainingSchedule(Document):
    def on_submit(self):

        if self.iscompleted:

            # Creating Training Schedule Feedback
            create_training_schedule_feedback(self)


            # Creating Certificate for every attendee on submit of Training schedule
            for attendee in self.attendees:
                year = int(attendee.get("validity"))
                days = year*365

                expiry_date = frappe.utils.add_days(attendee.get("issue_date"),days),
                attendee.expiry_date = expiry_date[0]
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
        else:
            frappe.throw(_("Mark the training schedule as complete first."))

    def validate(self):
        try:
            iqamaid_ = []
            dup_ele = []
            for row in self.attendees:
                dup_ele.append(row.iqamaid_no) if row.iqamaid_no in iqamaid_ else iqamaid_.append(row.iqamaid_no)

            if len(dup_ele) >0 :
                frappe.throw(_("Duplicate IQAMA/ID NO: {0} in Attendees Table.").format(frappe.bold(', '.join(str(x) for x in set(dup_ele)))))

        except Exception as e:
            raise e


    def after_save(self):
        # Creating Training Schedule calender
        create_training_schedule_calender(self)
@frappe.whitelist()
def create_training_schedule_calender(data):
    try:
        if isinstance(data,str):
            data = frappe.parse_json(data)
        print(data,"datataaa")    
        # ------------start For Delete existing TS Calender Doc ----------------
        ts_name = frappe.db.get_list("TS",filters={"training_schedule": data.name},pluck='name')
        for doc in ts_name:
            frappe.delete_doc("TS", doc)
        # ------------End For Delete existing TS Calender Doc ----------------

        start_obj = datetime.datetime.strptime(data.start_time, "%Y-%m-%d")
        end_obj = datetime.datetime.strptime(data.end_time, "%Y-%m-%d")

        # consider the start date as YYYY, mm, dd
        start_date = datetime.date(int(start_obj.strftime("%Y")), int(start_obj.strftime("%m")), int(start_obj.strftime("%d")))

        # consider the end date as YYYYY, mm, dd
        end_date = datetime.date(int(end_obj.strftime("%Y")), int(end_obj.strftime("%m")), int(end_obj.strftime("%d")))

        # delta time
        delta = datetime.timedelta(days=1)

        # iterate over range of dates
        while (start_date <= end_date):
            ts = frappe.new_doc("TS")
            ts.start_date = str(start_date) +" "+ str(data.starting_time)
            ts.end_date = str(start_date) +" "+ str(data.ending_time)
            ts.clientcustomer_name = data.clientcustomer_name
            ts.sales_order = data.sales_order
            ts.training_schedule = data.name
            ts.trainer = data.trainer
            ts.trainer_email = data.trainer_email
            ts.trainer_name = data.trainer_name
            ts.course = data.course
            ts.course_name = data.course_name
            if data.trainer_name and data.course_name:
                ts.course_and_trainer_name = data.trainer_name + " :-"+ data.course_name
            elif not data.trainer_name and data.course_name:
                ts.course_and_trainer_name =  data.course_name
            elif data.trainer_name and not data.course_name:
                ts.course_and_trainer_name =  data.trainer_name
            else:
                ts.course_and_trainer_name = ""


            ts.save()

            start_date += delta

    except Exception as e:
        raise

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
    
    # Fetching Item Details
    item_tax_template = ""
    item = frappe.get_doc("Item",training_schedule.course)
    for item_tax in item.taxes:
        item_tax_template = item_tax.item_tax_template

    
    # Creating Sales Invoice 
    sales_invoice = frappe.new_doc("Sales Invoice")
    sales_invoice.customer = sales_order_details.customer
    sales_invoice.training_schedule = docname
    sales_invoice.custom_cr_number = sales_order_details.custom_cr_number
    sales_invoice.custom_vat_number_ = sales_order_details.custom_vat_number
    sales_invoice.append("items",{
        "item_code":training_schedule.course,
        "qty":len(json_data["undefined"]),
        "amount":len(json_data["undefined"]) * training_schedule.course_amount,
        "custom_training_schedule": docname,
        "item_tax_template":item_tax_template if item_tax_template else ""
    })
    for attendee in json_data["undefined"]:
        sales_invoice.append("attendee",{
            "attendee_name":attendee.get("attendee_name"),
            "course":attendee.get("course"),
            "issue_date":attendee.get("issue_date"),
            "validity":attendee.get("validity"),
            "iqamaid_no":attendee.get("iqamaid_no")

        })
    sales_invoice.taxes_and_charges = sales_order_details.taxes_and_charges
    sales_invoice.taxes = sales_order_details.taxes
    sales_invoice.custom_location = sales_order_details.custom_location
    sales_invoice.tc_name = sales_order_details.tc_name
    sales_invoice.terms = sales_order_details.terms
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

@frappe.whitelist(allow_guest=True)
def get_training_schedule(sales_order):
    # data =frappe.db.sql("""
    #         SELECT name, clientcustomer_name as customer 
    #         FROM `tabTraining Schedule` 
    #         WHERE sales_order = '{0}'
    #         and docstatus!=2
    #         """.format(sales_order),as_dict=True)
    data = frappe.db.sql("""SELECT DISTINCT ts.name, ts.clientcustomer_name AS customer
                FROM `tabTraining Schedule` ts
                INNER JOIN `tabAttendees Table` at ON at.parent = ts.name
                WHERE (at.sales_invoice IS NULL or at.sales_invoice = "")
                AND ts.docstatus != 2
                AND ts.sales_order = '{0}';
                """.format(sales_order),as_dict=True)
    return data


@frappe.whitelist(allow_guest = True)
def get_attendee(values,sales_invoice):
    values = json.loads(values)
    names = [item['name'] for item in values]
    data = []
    data_item = []
    for tr in names:
        training_doc = frappe.get_doc("Training Schedule",tr)
        data_item.append({
            "item_code": training_doc.course,
            "custom_training_schedule": training_doc.name
        })
        if len(training_doc.attendees)==0:
            doc_link = f"<a href='{get_url('app/training-schedule/' + tr)}'>{tr}</a>"
            frappe.throw(f"Attendees are missing in training schedule {doc_link}")
        else:
            for attendee in training_doc.attendees:
                if not attendee.sales_invoice:
                    data.append({
                        'name': tr,
                        'course':training_doc.course,
                        'attendee_id': attendee.name,
                        'attendee_name': attendee.attendee_name,
                        'iqamaid_no': attendee.iqamaid_no,
                        'issue_date': attendee.issue_date,
                        'validity': attendee.validity,
                        'expiry_date': attendee.expiry_date,
                        'upload_photo': attendee.upload_photo,
                        'status': attendee.status
                    })

    return data, data_item