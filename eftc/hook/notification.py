import frappe


def quotation_follow_up_notofication():
            # Fetching All the Quotation Which are approved and notification is not sent for that
            quotations = frappe.get_all("Quotation" ,
                                        filters = {
                                                "workflow_state" : "Approved",
                                                "docstatus":1,
                                                "is_notified":0
                                                },
                                         fields = [
                                                 "name" , "creation" , "owner" , "modified" 
                                                ])
            for quotation in quotations:
                # Checking Quotations which are approved 2 days ago
                if frappe.utils.now_datetime() < frappe.utils.add_days(quotation["modified"],2):
                    notification = frappe.get_doc({
                            "doctype": "Notification Log",
                            "subject": "Please Take Follow Up On <strong> {} </strong>".format(quotation["name"]),
                            "for_user": quotation["owner"],
                            "document_type": "Quotation",
                            "document_name":quotation["name"],
                            "read": 0
                        })
                    notification.insert(ignore_permissions=True)

                # Setting is_notified 1 in quotation     
                frappe.db.set_value('Quotation', quotation["name"], 'is_notified', 0, update_modified=False)

 