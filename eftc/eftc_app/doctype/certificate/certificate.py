# Copyright (c) 2023, NestorBird and contributors
# For license information, please see license.txt

import frappe
import io
import os
from erpnext import get_default_company
from frappe import _
from pyqrcode import create as qr_create
from base64 import b64encode
import datetime
from frappe.model.document import Document

class Certificate(Document):
	def after_insert(self):
		# Converting String Date into Datetime 
		expiry_date = datetime.datetime(2023, 8, 24, 2, 24)
		

		# Setting Expiry Date for QR Code 
		full_data = f"{self.qr_code_url}expiry_date={expiry_date.isoformat()}"
		qr_image = io.BytesIO()
		url = qr_create(full_data)
		url.png(qr_image, scale=2, quiet_zone=1)
		name = frappe.generate_hash(self.name, 5)
		filename = f"QRCode-{name}.png".replace(os.path.sep, "__")

		# Saving In File Doctype
		_file = frappe.get_doc(
				{
					"doctype": "File",
					"file_name":filename,
					"is_private": 0,
					"content": qr_image.getvalue(),
					"attached_to_doctype": "Certificate",
					"attached_to_name":self.name,
					"attached_to_field": "qr_image"
				}
			)

		_file.save()

		# Updating QR image in Certificate
		self.db_set("qr_image", _file.file_url)


def abc():
	current_date = frappe.utils.today()
	print(current_date)