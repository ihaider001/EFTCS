import frappe

@frappe.whitelist()
def set_qr_code_url(name):
    url = frappe.utils.get_url()+"/printview?doctype=Quotation&name={0}&format=Standard&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en".format(name)
    frappe.db.set_value('Quotation', name, 'qr_code_url', url, update_modified=False)

