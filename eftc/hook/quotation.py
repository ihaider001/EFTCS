import frappe
import io
import os
from erpnext import get_default_company
from frappe import _
from pyqrcode import create as qr_create
from base64 import b64encode
import datetime 
from frappe.utils import today

@frappe.whitelist()
def set_qr_code_url(doctype,docname,print_format , field_name ):
    url = frappe.utils.get_url()+"/api/method/frappe.utils.print_format.download_pdf?doctype={doctype}&name={docname}&format={print_format}&no_letterhead=0&letterhead=EFTC%20Letter%20Head&settings=%7B%7D&_lang=en".format(
        doctype = doctype ,
          docname = docname,
          print_format = print_format
          )
    frappe.db.set_value(doctype, docname, field_name, url, update_modified=False)


def generate_qr_code(doc,method):

    # Adding Date to Current Date 
    current_date = today()
    validity_date = frappe.utils.add_days(current_date,int(doc.qr_code_validity_in_days))

    # Converting String Date into Datetime 
    expiry_date = datetime.datetime.strptime(validity_date, "%Y-%m-%d")


    # Setting Expiry date for qr code 
    full_data = f"{doc.qr_code_url}expiry_date={expiry_date.isoformat()}"
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