import frappe
import io
import os
from erpnext import get_default_company
from frappe import _
from pyqrcode import create as qr_create
from base64 import b64encode
import datetime 
from frappe.utils import today
from eftc.hook.sales_invoice import money_in_words_arabic


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
				"attached_to_doctype": "Purchase Order",
				"attached_to_name":doc.name,
                "attached_to_field": "qr_image",
			}
		)

    _file.save()

    # assigning to document
    doc.db_set("qr_image", _file.file_url)

def convert_number(doc,method):
    words = money_in_words_arabic(doc.grand_total, doc.currency)
    doc.custom_in_wordsarabic = words
    doc.save()

def after_insert(doc,method):
    from eftc.hook.quotation import set_qr_code_url
    url=set_qr_code_url("Purchase Order",doc.name,"Purchase Order","qr_code_url")
    doc.qr_code_url=url
    doc.save()