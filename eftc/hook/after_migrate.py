import frappe

def main():
    set_item_naming_series()

def set_item_naming_series():
    stock_setting = frappe.get_doc("Stock Settings")
    stock_setting.item_naming_by = "Naming Series"
    stock_setting.save()