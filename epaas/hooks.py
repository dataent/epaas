from __future__ import unicode_literals
from dataent import _

app_name = "epaas"
app_title = "EPAAS"
app_publisher = "Dataent Technologies Pvt. Ltd."
app_description = """ERP made simple"""
app_icon = "fa fa-th"
app_color = "#e74c3c"
app_email = "info@epaas.xyz"
app_license = "GNU General Public License (v3)"
source_link = "https://github.com/dataent/epaas"

develop_version = '12.x.x-develop'

app_include_js = "assets/js/epaas.min.js"
app_include_css = "assets/css/epaas.css"
web_include_js = "assets/js/epaas-web.min.js"
web_include_css = "assets/css/epaas-web.css"

doctype_js = {
	"Communication": "public/js/communication.js",
	"Event": "public/js/event.js"
}

welcome_email = "epaas.setup.utils.welcome_email"

# setup wizard
setup_wizard_requires = "assets/epaas/js/setup_wizard.js"
setup_wizard_stages = "epaas.setup.setup_wizard.setup_wizard.get_setup_stages"
setup_wizard_test = "epaas.setup.setup_wizard.test_setup_wizard.run_setup_wizard_test"

before_install = "epaas.setup.install.check_setup_wizard_not_completed"
after_install = "epaas.setup.install.after_install"

boot_session = "epaas.startup.boot.boot_session"
notification_config = "epaas.startup.notifications.get_notification_config"
get_help_messages = "epaas.utilities.activation.get_help_messages"
get_user_progress_slides = "epaas.utilities.user_progress.get_user_progress_slides"
update_and_get_user_progress = "epaas.utilities.user_progress_utils.update_default_domain_actions_and_get_state"

on_session_creation = "epaas.shopping_cart.utils.set_cart_count"
on_logout = "epaas.shopping_cart.utils.clear_cart_count"

treeviews = ['Account', 'Cost Center', 'Warehouse', 'Item Group', 'Customer Group', 'Sales Person', 'Territory', 'Assessment Group', 'Department']

# website
update_website_context = "epaas.shopping_cart.utils.update_website_context"
my_account_context = "epaas.shopping_cart.utils.update_my_account_context"

email_append_to = ["Job Applicant", "Lead", "Opportunity", "Issue"]

calendars = ["Task", "Work Order", "Leave Application", "Sales Order", "Holiday List", "Course Schedule"]



domains = {
	'Agriculture': 'epaas.domains.agriculture',
	'Distribution': 'epaas.domains.distribution',
	'Education': 'epaas.domains.education',
	'Healthcare': 'epaas.domains.healthcare',
	'Hospitality': 'epaas.domains.hospitality',
	'Manufacturing': 'epaas.domains.manufacturing',
	'Non Profit': 'epaas.domains.non_profit',
	'Retail': 'epaas.domains.retail',
	'Services': 'epaas.domains.services',
}

website_generators = ["Item Group", "Item", "BOM", "Sales Partner",
	"Job Opening", "Student Admission"]

website_context = {
	"favicon": 	"/assets/epaas/images/favicon.png",
	"splash_image": "/assets/epaas/images/erp-icon.svg"
}

website_route_rules = [
	{"from_route": "/orders", "to_route": "Sales Order"},
	{"from_route": "/orders/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Sales Order",
			"parents": [{"label": _("Orders"), "route": "orders"}]
		}
	},
	{"from_route": "/invoices", "to_route": "Sales Invoice"},
	{"from_route": "/invoices/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Sales Invoice",
			"parents": [{"label": _("Invoices"), "route": "invoices"}]
		}
	},
	{"from_route": "/supplier-quotations", "to_route": "Supplier Quotation"},
	{"from_route": "/supplier-quotations/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Supplier Quotation",
			"parents": [{"label": _("Supplier Quotation"), "route": "supplier-quotations"}]
		}
	},
	{"from_route": "/quotations", "to_route": "Quotation"},
	{"from_route": "/quotations/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Quotation",
			"parents": [{"label": _("Quotations"), "route": "quotations"}]
		}
	},
	{"from_route": "/shipments", "to_route": "Delivery Note"},
	{"from_route": "/shipments/<path:name>", "to_route": "order",
		"defaults": {
			"doctype": "Delivery Note",
			"parents": [{"label": _("Shipments"), "route": "shipments"}]
		}
	},
	{"from_route": "/rfq", "to_route": "Request for Quotation"},
	{"from_route": "/rfq/<path:name>", "to_route": "rfq",
		"defaults": {
			"doctype": "Request for Quotation",
			"parents": [{"label": _("Request for Quotation"), "route": "rfq"}]
		}
	},
	{"from_route": "/addresses", "to_route": "Address"},
	{"from_route": "/addresses/<path:name>", "to_route": "addresses",
		"defaults": {
			"doctype": "Address",
			"parents": [{"label": _("Addresses"), "route": "addresses"}]
		}
	},
	{"from_route": "/jobs", "to_route": "Job Opening"},
	{"from_route": "/admissions", "to_route": "Student Admission"},
	{"from_route": "/boms", "to_route": "BOM"},
	{"from_route": "/timesheets", "to_route": "Timesheet"},
]

standard_portal_menu_items = [
	{"title": _("Personal Details"), "route": "/personal-details", "reference_doctype": "Patient", "role": "Patient"},
	{"title": _("Projects"), "route": "/project", "reference_doctype": "Project"},
	{"title": _("Request for Quotations"), "route": "/rfq", "reference_doctype": "Request for Quotation", "role": "Supplier"},
	{"title": _("Supplier Quotation"), "route": "/supplier-quotations", "reference_doctype": "Supplier Quotation", "role": "Supplier"},
	{"title": _("Quotations"), "route": "/quotations", "reference_doctype": "Quotation", "role":"Customer"},
	{"title": _("Orders"), "route": "/orders", "reference_doctype": "Sales Order", "role":"Customer"},
	{"title": _("Invoices"), "route": "/invoices", "reference_doctype": "Sales Invoice", "role":"Customer"},
	{"title": _("Shipments"), "route": "/shipments", "reference_doctype": "Delivery Note", "role":"Customer"},
	{"title": _("Issues"), "route": "/issues", "reference_doctype": "Issue", "role":"Customer"},
	{"title": _("Addresses"), "route": "/addresses", "reference_doctype": "Address"},
	{"title": _("Timesheets"), "route": "/timesheets", "reference_doctype": "Timesheet", "role":"Customer"},
	{"title": _("Timesheets"), "route": "/timesheets", "reference_doctype": "Timesheet", "role":"Customer"},
	{"title": _("Lab Test"), "route": "/lab-test", "reference_doctype": "Lab Test", "role":"Patient"},
	{"title": _("Prescription"), "route": "/prescription", "reference_doctype": "Patient Encounter", "role":"Patient"},
	{"title": _("Patient Appointment"), "route": "/patient-appointments", "reference_doctype": "Patient Appointment", "role":"Patient"},
	{"title": _("Fees"), "route": "/fees", "reference_doctype": "Fees", "role":"Student"},
	{"title": _("Newsletter"), "route": "/newsletters", "reference_doctype": "Newsletter"},
	{"title": _("Admission"), "route": "/admissions", "reference_doctype": "Student Admission"},
	{"title": _("Certification"), "route": "/certification", "reference_doctype": "Certification Application"},
]

default_roles = [
	{'role': 'Customer', 'doctype':'Contact', 'email_field': 'email_id'},
	{'role': 'Supplier', 'doctype':'Contact', 'email_field': 'email_id'},
	{'role': 'Student', 'doctype':'Student', 'email_field': 'student_email_id'},
]

has_website_permission = {
	"Sales Order": "epaas.controllers.website_list_for_contact.has_website_permission",
	"Quotation": "epaas.controllers.website_list_for_contact.has_website_permission",
	"Sales Invoice": "epaas.controllers.website_list_for_contact.has_website_permission",
	"Supplier Quotation": "epaas.controllers.website_list_for_contact.has_website_permission",
	"Delivery Note": "epaas.controllers.website_list_for_contact.has_website_permission",
	"Issue": "epaas.support.doctype.issue.issue.has_website_permission",
	"Timesheet": "epaas.controllers.website_list_for_contact.has_website_permission",
	"Lab Test": "epaas.healthcare.web_form.lab_test.lab_test.has_website_permission",
	"Patient Encounter": "epaas.healthcare.web_form.prescription.prescription.has_website_permission",
	"Patient Appointment": "epaas.healthcare.web_form.patient_appointments.patient_appointments.has_website_permission",
	"Patient": "epaas.healthcare.web_form.personal_details.personal_details.has_website_permission"
}

dump_report_map = "epaas.startup.report_data_map.data_map"

before_tests = "epaas.setup.utils.before_tests"

standard_queries = {
	"Customer": "epaas.selling.doctype.customer.customer.get_customer_list",
	"Healthcare Practitioner": "epaas.healthcare.doctype.healthcare_practitioner.healthcare_practitioner.get_practitioner_list"
}

doc_events = {
	"Stock Entry": {
		"on_submit": "epaas.stock.doctype.material_request.material_request.update_completed_and_requested_qty",
		"on_cancel": "epaas.stock.doctype.material_request.material_request.update_completed_and_requested_qty"
	},
	"User": {
		"after_insert": "dataent.contacts.doctype.contact.contact.update_contact",
		"validate": "epaas.hr.doctype.employee.employee.validate_employee_role",
		"on_update": ["epaas.hr.doctype.employee.employee.update_user_permissions",
			"epaas.portal.utils.set_default_role"]
	},
	("Sales Taxes and Charges Template", 'Price List'): {
		"on_update": "epaas.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings.validate_cart_settings"
	},

	"Website Settings": {
		"validate": "epaas.portal.doctype.products_settings.products_settings.home_page_is_products"
	},
	"Sales Invoice": {
		"on_submit": ["epaas.regional.france.utils.create_transaction_log", "epaas.regional.italy.utils.sales_invoice_on_submit"],
		"on_cancel": "epaas.regional.italy.utils.sales_invoice_on_cancel",
		"on_trash": "epaas.regional.check_deletion_permission"
	},
	"Payment Entry": {
		"on_submit": ["epaas.regional.france.utils.create_transaction_log", "epaas.accounts.doctype.payment_request.payment_request.make_status_as_paid"],
		"on_trash": "epaas.regional.check_deletion_permission"
	},
	'Address': {
		'validate': ['epaas.regional.india.utils.validate_gstin_for_india', 'epaas.regional.italy.utils.set_state_code']
	},
	('Sales Invoice', 'Purchase Invoice', 'Delivery Note'): {
		'validate': 'epaas.regional.india.utils.set_place_of_supply'
	},
	"Contact":{
		"on_trash": "epaas.support.doctype.issue.issue.update_issue"
	}
}

scheduler_events = {
	"all": [
		"epaas.projects.doctype.project.project.project_status_update_reminder"
	],
	"hourly": [
		'epaas.hr.doctype.daily_work_summary_group.daily_work_summary_group.trigger_emails',
		"epaas.accounts.doctype.subscription.subscription.process_all",
		"epaas.epaas_integrations.doctype.amazon_mws_settings.amazon_mws_settings.schedule_get_order_details",
		"epaas.epaas_integrations.doctype.plaid_settings.plaid_settings.automatic_synchronization",
		"epaas.projects.doctype.project.project.hourly_reminder",
		"epaas.projects.doctype.project.project.collect_project_status"
	],
	"daily": [
		"epaas.stock.reorder_item.reorder_item",
		"epaas.setup.doctype.email_digest.email_digest.send",
		"epaas.support.doctype.issue.issue.auto_close_tickets",
		"epaas.crm.doctype.opportunity.opportunity.auto_close_opportunity",
		"epaas.controllers.accounts_controller.update_invoice_status",
		"epaas.accounts.doctype.fiscal_year.fiscal_year.auto_create_fiscal_year",
		"epaas.hr.doctype.employee.employee.send_birthday_reminders",
		"epaas.projects.doctype.task.task.set_tasks_as_overdue",
		"epaas.assets.doctype.asset.depreciation.post_depreciation_entries",
		"epaas.hr.doctype.daily_work_summary_group.daily_work_summary_group.send_summary",
		"epaas.stock.doctype.serial_no.serial_no.update_maintenance_status",
		"epaas.buying.doctype.supplier_scorecard.supplier_scorecard.refresh_scorecards",
		"epaas.setup.doctype.company.company.cache_companies_monthly_sales_history",
		"epaas.assets.doctype.asset.asset.update_maintenance_status",
		"epaas.assets.doctype.asset.asset.make_post_gl_entry",
		"epaas.crm.doctype.contract.contract.update_status_for_contracts",
		"epaas.projects.doctype.project.project.update_project_sales_billing",
		"epaas.projects.doctype.project.project.send_project_status_email_to_users"
	],
	"daily_long": [
		"epaas.manufacturing.doctype.bom_update_tool.bom_update_tool.update_latest_price_in_all_boms"
	],
	"monthly_long": [
		"epaas.accounts.deferred_revenue.convert_deferred_revenue_to_income",
		"epaas.accounts.deferred_revenue.convert_deferred_expense_to_expense",
		"epaas.hr.utils.allocate_earned_leaves"
	]
}

email_brand_image = "assets/epaas/images/epaas-logo.jpg"

default_mail_footer = """
	<span>
		Sent via
		<a class="text-muted" href="https://epaas.xyz?source=via_email_footer" target="_blank">
			EPAAS
		</a>
	</span>
"""

get_translated_dict = {
	("doctype", "Global Defaults"): "dataent.geo.country_info.get_translated_dict"
}

bot_parsers = [
	'epaas.utilities.bot.FindItemBot',
]

get_site_info = 'epaas.utilities.get_site_info'

payment_gateway_enabled = "epaas.accounts.utils.create_payment_gateway_account"

regional_overrides = {
	'France': {
		'epaas.tests.test_regional.test_method': 'epaas.regional.france.utils.test_method'
	},
	'India': {
		'epaas.tests.test_regional.test_method': 'epaas.regional.india.utils.test_method',
		'epaas.controllers.taxes_and_totals.get_itemised_tax_breakup_header': 'epaas.regional.india.utils.get_itemised_tax_breakup_header',
		'epaas.controllers.taxes_and_totals.get_itemised_tax_breakup_data': 'epaas.regional.india.utils.get_itemised_tax_breakup_data',
		'epaas.accounts.party.get_regional_address_details': 'epaas.regional.india.utils.get_regional_address_details',
		'epaas.hr.utils.calculate_annual_eligible_hra_exemption': 'epaas.regional.india.utils.calculate_annual_eligible_hra_exemption',
		'epaas.hr.utils.calculate_hra_exemption_for_period': 'epaas.regional.india.utils.calculate_hra_exemption_for_period'
	},
	'United Arab Emirates': {
		'epaas.controllers.taxes_and_totals.update_itemised_tax_data': 'epaas.regional.united_arab_emirates.utils.update_itemised_tax_data'
	},
	'Saudi Arabia': {
		'epaas.controllers.taxes_and_totals.update_itemised_tax_data': 'epaas.regional.united_arab_emirates.utils.update_itemised_tax_data'
	},
	'Italy': {
		'epaas.controllers.taxes_and_totals.update_itemised_tax_data': 'epaas.regional.italy.utils.update_itemised_tax_data',
		'epaas.controllers.accounts_controller.validate_regional': 'epaas.regional.italy.utils.sales_invoice_validate',
	}
}
