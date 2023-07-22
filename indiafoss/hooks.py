from . import __version__ as app_version

app_name = "indiafoss"
app_title = "Indiafoss"
app_publisher = "shridhar.p@zerodha.com"
app_description = (
    "Free and Open Source Software conference by the FOSS United community."
)
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shridhar.p@zerodha..com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/indiafoss/css/indiafoss.css"
# app_include_js = "/assets/indiafoss/js/indiafoss.js"

# include js, css files in header of web template
# web_include_css = "/assets/indiafoss/css/indiafoss.css"
# web_include_js = "/assets/indiafoss/js/indiafoss.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "indiafoss/public/scss/website"

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

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "indiafoss.utils.jinja_methods",
# 	"filters": "indiafoss.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "indiafoss.install.before_install"
# after_install = "indiafoss.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "indiafoss.uninstall.before_uninstall"
# after_uninstall = "indiafoss.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "indiafoss.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"indiafoss.tasks.all"
# 	],
# 	"daily": [
# 		"indiafoss.tasks.daily"
# 	],
# 	"hourly": [
# 		"indiafoss.tasks.hourly"
# 	],
# 	"weekly": [
# 		"indiafoss.tasks.weekly"
# 	],
# 	"monthly": [
# 		"indiafoss.tasks.monthly"
# 	],
# }

scheduler_events = {
    "all": [
        "indiafoss.tasks.capture_pending_payments",
    ],
}

# Testing
# -------

# before_tests = "indiafoss.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "indiafoss.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "indiafoss.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"indiafoss.auth.validate"
# ]


fixtures = [
    {"dt": "Web Page", "filters": [["module", "in", ("Indiafoss")]]},
    {"dt": "Web Template", "filters": [["module", "in", ("Indiafoss")]]},
    {"dt": "Web Form", "filters": [["module", "in", ("Indiafoss")]]},
]
