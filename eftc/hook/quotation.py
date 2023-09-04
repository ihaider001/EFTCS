import frappe
import io
import os
from erpnext import get_default_company
from frappe import _
from pyqrcode import create as qr_create
from base64 import b64encode
import datetime 
from frappe.utils import today , add_to_date ,getdate
from datetime import datetime

@frappe.whitelist()
def set_qr_code_url(doctype,docname,print_format , field_name ):
    url = frappe.utils.get_url()+"/api/method/eftc.hook.quotation.qr_code_scanning_with_validation?doctype={doctype}&name={docname}&format={print_format}".format(
        doctype = doctype ,
          docname = docname,
          print_format = print_format
          )
    frappe.db.set_value(doctype, docname, field_name, url, update_modified=False)


def generate_qr_code(doc,method):

    # Setting Expiry date for qr code 
    full_data = doc.qr_code_url
    qr_image = io.BytesIO()
    url = qr_create(full_data)
    url.png(qr_image, scale=2, quiet_zone=1)
    name = frappe.generate_hash(doc.name, 5)
    filename = f"QRCode-{name}.png".replace(os.path.sep, "__")

    _file = frappe.get_doc(
			{
				"doctype": "File",
				"file_name":filename,
				"is_private": 0,
				"content": qr_image.getvalue(),
				"attached_to_doctype": "Quotation",
				"attached_to_name":doc.name,
                "attached_to_field": "qr_image",
			}
		)

    _file.save()

    # assigning to document
    doc.db_set("qr_image", _file.file_url)


@frappe.whitelist(allow_guest = True)
def qr_code_scanning_with_validation():
    try:
        #  Fetching Arguments From Api
        args =  args = frappe.local.request.args 
        print_format_url = "/api/method/frappe.utils.print_format.download_pdf?doctype={doctype}&name={docname}&format={print_format}&no_letterhead=0&letterhead=EFTC%20Letter%20Head&settings=%7B%7D&_lang=en".format(
                                doctype = args.get("doctype") ,
                                docname = args.get("name"),
                                print_format = args.get("format")
                                )

        if args.get("doctype") == "Quotation":
            quotation = frappe.get_doc("Quotation",args.get("name"))

            # Getting Valid Upto Date of QR code
            valid_upto = add_to_date(quotation.modified, days=int(quotation.qr_code_validity_in_days),  as_datetime=True)  

            if datetime.now() < valid_upto :
                frappe.local.response["http_status_code"] = 303
                frappe.local.response["type"] = "redirect"
                frappe.local.response["location"] = print_format_url
            
            else :
                frappe.local.response["http_status_code"] = 498
                return "QR Code Expired"
            
        elif args.get("doctype") == "Purchase Order" or args.get("doctype") == "Purchase Invoice":
            data = frappe.get_doc(args.get("doctype"),args.get("name"))

             # Getting Valid Upto Date of QR code
            valid_upto = add_to_date(data.modified, days=int(data.custom_qr_code_validity_in_days),  as_datetime=True)  

            if datetime.now() < valid_upto :
                frappe.local.response["http_status_code"] = 303
                frappe.local.response["type"] = "redirect"
                frappe.local.response["location"] = print_format_url
            
            else :
                frappe.local.response["http_status_code"] = 498
                return "QR Code Expired"

        elif args.get("doctype") == "Certificate":
            certificate = frappe.get_doc("Certificate",args.get("name")) 
            if getdate() < certificate.expiry :
                frappe.local.response["http_status_code"] = 303
                frappe.local.response["type"] = "redirect"
                frappe.local.response["location"] = print_format_url
            
            else :
                frappe.local.response["http_status_code"] = 498
                return "QR Code Expired"
                

        else:
            return "QR Code Not Found"    

    except Exception  as e:
        return e

