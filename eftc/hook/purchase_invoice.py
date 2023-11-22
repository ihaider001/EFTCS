import frappe
import io
import os
from erpnext import get_default_company
from frappe import _
from pyqrcode import create as qr_create
from base64 import b64encode
import datetime 
from frappe.utils import today




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
				"attached_to_doctype": "Purchase Invoice",
				"attached_to_name":doc.name,
                "attached_to_field": "qr_image",
			}
		)

    _file.save()

    # assigning to document
    doc.db_set("qr_image", _file.file_url)

def after_insert(doc,method):
    from eftc.hook.quotation import set_qr_code_url
    url=set_qr_code_url("Purchase Invoice",doc.name,"Purchase Return","qr_code_url")
    doc.qr_code_url=url
    doc.save()
