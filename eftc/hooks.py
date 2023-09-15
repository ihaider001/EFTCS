from . import __version__ as app_version

app_name = "eftc"
app_title = "EFTC APP"
app_publisher = "NestorBird"
app_description = "EFTC APP"
app_email = "info@nestorbird.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/eftc/css/eftc.css"
# app_include_js = "/assets/eftc/js/eftc.js"

# include js, css files in header of web template
# web_include_css = "/assets/eftc/css/eftc.css"
# web_include_js = "/assets/eftc/js/eftc.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "eftc/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

doctype_list_js={
    "Training Schedule" :"public/js/training_list.js",
    "Certificate" :"public/js/certificate_list.js"
}

doctype_js = {
    "Quotation":"public/js/quotation.js",
    "Purchase Invoice":"public/js/purchase_invoice.js",
    "Purchase Order":"public/js/purchase_order.js",
    "Training Schedule":"public/js/training.js",
    "Sales Invoice":"public/js/sales_invoice.js"
}
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "eftc.utils.jinja_methods",
#	"filters": "eftc.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "eftc.install.before_install"
# after_install = "eftc.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "eftc.uninstall.before_uninstall"
# after_uninstall = "eftc.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "eftc.utils.before_app_install"
# after_app_install = "eftc.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "eftc.utils.before_app_uninstall"
# after_app_uninstall = "eftc.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "eftc.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "Sales Order":{
        "on_submit":"eftc.hook.sales_order.on_submit"
    },
    "Quotation":{
        "on_submit":"eftc.hook.quotation.generate_qr_code"
    },
    "Purchase Invoice":{
        "on_submit":"eftc.hook.purchase_invoice.generate_qr_code"
    },
    "Purchase Order":{
        "on_submit":"eftc.hook.purchase_order.generate_qr_code"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"eftc.tasks.all"
#	],
#	"daily": [
#		"eftc.tasks.daily"
#	],
#	"hourly": [
#		"eftc.tasks.hourly"
#	],
#	"weekly": [
#		"eftc.tasks.weekly"
#	],
#	"monthly": [
#		"eftc.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "eftc.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.selling.doctype.quotation.quotation.make_sales_order": "eftc.overrides.quotation.make_sales_order"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "eftc.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["eftc.utils.before_request"]
# after_request = ["eftc.utils.after_request"]

# Job Events
# ----------
# before_job = ["eftc.utils.before_job"]
# after_job = ["eftc.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"eftc.auth.validate"
# ]
fixtures = [
     {
        "dt": "Custom Field", "filters":
        [
            [
                "name", "in", [
                    "Quotation-cr_number",
                    "Quotation-vat_number",
                    "is_notified",
                    "Quotation-qr_code_url",
                    "Item-zone",
                    "Item-subgroup",
                    "Sales Invoice-attendee",
                    "Sales Invoice-attendee_data",
                    "Sales Invoice-training_schedule",
                    "Quotation-qr_image",
                    "Quotation-qr_code_validity_in_days",
                    "Purchase Order-qr_image",
                    "Purchase Order-qr_code_url",
                    "Purchase Invoice-qr_code_url",
                    "Purchase Invoice-qr_image",
                    "Sales Invoice Item-awarding_body",
                    "Sales Order Item-awarding_body",
                    "Quotation Item-awarding_body",
                    "Quotation-customer_name_in_arabic",
                    "Item-item_name_in_arabic",
                    "Quotation-custom_sales_representative",
                    "Quotation-sales_representative_mobile_number",
                    "Quotation-training_mode",
                    "Quotation-location",
                    "Address-cr_no_in_arabic",
                    "Address-cr_no",
                    "Address-vat_number_in_arabic",
                    "Address-vat_number_",
                    "Address-arabic_coutry",
                    "Address-postal_code_in_arabic",
                    "Address-state_province_in_arabic",
                    "Address-city__time_in_arabic",
                    "Address-address_line_2_in_arabic",
                    "Address-address_title_in_arabic_",
                    "Address-address_in_arabic",
                    "Address-phone_in_arabic",
                    "Purchase Order-custom_qr_code_validity_in_days",
                    "Purchase Invoice-custom_qr_code_validity_in_days",
                    "Sales Order-custom_cr_number",
                    "Sales Order-custom_vat_number",
                    "Sales Order-custom_from_date_",
                    "Sales Invoice-custom_cr_number",
                    "Sales Invoice-custom_vat_number_",
                    "Sales Order-custom_training_mode_",
                    "Sales Order-custom_training_mode_",
                    "Sales Invoice Item-custom_item_name_in_arabic",
                    "Item-custom_duration"
                ]]  
        ]},
         {
        "dt": "Workflow State", "filters":
        [
            [
                "name", "in", [
                   "In Review",
                   "Require Change",
                   "Draft"
                ]]  
        ]},
        {
        "dt": "Workflow Action Master", "filters":
        [
            [
                "name", "in", [
                  "Require Change",
                  "Save"
                ]]  
        ]},
        {
        "dt": "Workflow", "filters":
        [
            [
                "name", "in", [
                    "Quotation",
                    "Purchase Order Workflow"
                ]]  
        ]},
        {
        "dt": "Property Setter", "filters":
        [
            [
                "name", "in", [
                   "Sales Invoice-main-links_order",
                   "Sales Order-main-links_order",
                   "Address-address_line2-label",
                   "Address-address_line1-label",
                   "Address-county-hidden",
                   "Sales Order-delivery_date-label",
                   "Quotation-total_qty-hidden",
                   "Quotation-shipping_rule-hidden",
                   "Quotation-incoterm-hidden",
                   "Sales Order-total_qty-hidden",
                   "Sales Order-shipping_rule-hidden",
                   "Sales Order-incoterm-hidden",
                   "Sales Invoice-total_qty-hidden",
                   "Sales Invoice-shipping_rule-hidden",
                   "Sales Invoice-incoterm-hidden"
                   
                ]]  
        ]},
        {
               "dt": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                   "Operation Manager"
                ]
            ]
        ]
    },
    {
        "dt": "Calendar View",
        "filters": [
            [
                "name",
                "in",
                [
                   "Training Schedule List"
                ]
            ]
        ]
    },
     {
        "dt": "Workspace",
        "filters": [
            [
                "name",
                "in",
                [
                   "Home"
                ]
            ]
        ]
    },

]



scheduler_events = {
	"cron": {
		"0/15 * * * *": [
			"eftc.hook.notification.quotation_follow_up_notofication"
		]
    }
}



after_migrate="eftc.hook.after_migrate.main"