
from __future__ import unicode_literals
import dataent, base64, hashlib, hmac, json
import datetime
from dataent import _


def verify_request():
	woocommerce_settings = dataent.get_doc("Woocommerce Settings")
	sig = base64.b64encode(
		hmac.new(
			woocommerce_settings.secret.encode('utf8'),
			dataent.request.data,
			hashlib.sha256
		).digest()
	)

	if dataent.request.data and \
		dataent.get_request_header("X-Wc-Webhook-Signature") and \
		not sig == bytes(dataent.get_request_header("X-Wc-Webhook-Signature").encode()):
			dataent.throw(_("Unverified Webhook Data"))
	dataent.set_user(woocommerce_settings.creation_user)

@dataent.whitelist(allow_guest=True)
def order(*args, **kwargs):
	try:
		_order(*args, **kwargs)
	except Exception:
		error_message = dataent.get_traceback()+"\n\n Request Data: \n"+json.loads(dataent.request.data).__str__()
		dataent.log_error(error_message, "WooCommerce Error")
		raise


def _order(*args, **kwargs):
	woocommerce_settings = dataent.get_doc("Woocommerce Settings")
	if dataent.flags.woocomm_test_order_data:
		fd = dataent.flags.woocomm_test_order_data
		event = "created"

	elif dataent.request and dataent.request.data:
		verify_request()
		fd = json.loads(dataent.request.data)
		event = dataent.get_request_header("X-Wc-Webhook-Event")

	else:
		return "success"

	if event == "created":
		raw_billing_data = fd.get("billing")
		customer_woo_com_email = raw_billing_data.get("email")

		if dataent.get_value("Customer",{"woocommerce_email": customer_woo_com_email}):
			# Edit
			link_customer_and_address(raw_billing_data,1)
		else:
			# Create
			link_customer_and_address(raw_billing_data,0)


		items_list = fd.get("line_items")
		for item in items_list:

			item_woo_com_id = item.get("product_id")

			if dataent.get_value("Item",{"woocommerce_id": item_woo_com_id}):
				#Edit
				link_item(item,1)
			else:
				link_item(item,0)


		customer_name = raw_billing_data.get("first_name") + " " + raw_billing_data.get("last_name")

		new_sales_order = dataent.new_doc("Sales Order")
		new_sales_order.customer = customer_name

		created_date = fd.get("date_created").split("T")
		new_sales_order.transaction_date = created_date[0]

		new_sales_order.po_no = fd.get("id")
		new_sales_order.woocommerce_id = fd.get("id")
		new_sales_order.naming_series = woocommerce_settings.sales_order_series or "SO-WOO-"

		placed_order_date = created_date[0]
		raw_date = datetime.datetime.strptime(placed_order_date, "%Y-%m-%d")
		raw_delivery_date = dataent.utils.add_to_date(raw_date,days = 7)
		order_delivery_date_str = raw_delivery_date.strftime('%Y-%m-%d')
		order_delivery_date = str(order_delivery_date_str)

		new_sales_order.delivery_date = order_delivery_date
		default_set_company = dataent.get_doc("Global Defaults")
		company = raw_billing_data.get("company") or default_set_company.default_company
		found_company = dataent.get_doc("Company",{"name":company})
		company_abbr = found_company.abbr

		new_sales_order.company = company

		for item in items_list:
			woocomm_item_id = item.get("product_id")
			found_item = dataent.get_doc("Item",{"woocommerce_id": woocomm_item_id})

			ordered_items_tax = item.get("total_tax")

			new_sales_order.append("items",{
				"item_code": found_item.item_code,
				"item_name": found_item.item_name,
				"description": found_item.item_name,
				"delivery_date":order_delivery_date,
				"uom": woocommerce_settings.uom or _("Nos"),
				"qty": item.get("quantity"),
				"rate": item.get("price"),
				"warehouse": woocommerce_settings.warehouse or "Stores" + " - " + company_abbr
				})

			add_tax_details(new_sales_order,ordered_items_tax,"Ordered Item tax",0)

		# shipping_details = fd.get("shipping_lines") # used for detailed order
		shipping_total = fd.get("shipping_total")
		shipping_tax = fd.get("shipping_tax")

		add_tax_details(new_sales_order,shipping_tax,"Shipping Tax",1)
		add_tax_details(new_sales_order,shipping_total,"Shipping Total",1)

		new_sales_order.submit()

		dataent.db.commit()

def link_customer_and_address(raw_billing_data,customer_status):

	if customer_status == 0:
		# create
		customer = dataent.new_doc("Customer")
		address = dataent.new_doc("Address")

	if customer_status == 1:
		# Edit
		customer_woo_com_email = raw_billing_data.get("email")
		customer = dataent.get_doc("Customer",{"woocommerce_email": customer_woo_com_email})
		old_name = customer.customer_name

	full_name = str(raw_billing_data.get("first_name"))+ " "+str(raw_billing_data.get("last_name"))
	customer.customer_name = full_name
	customer.woocommerce_email = str(raw_billing_data.get("email"))
	customer.save()
	dataent.db.commit()

	if customer_status == 1:
		dataent.rename_doc("Customer", old_name, full_name)
		address = dataent.get_doc("Address",{"woocommerce_email":customer_woo_com_email})
		customer = dataent.get_doc("Customer",{"woocommerce_email": customer_woo_com_email})

	address.address_line1 = raw_billing_data.get("address_1", "Not Provided")
	address.address_line2 = raw_billing_data.get("address_2", "Not Provided")
	address.city = raw_billing_data.get("city", "Not Provided")
	address.woocommerce_email = str(raw_billing_data.get("email"))
	address.address_type = "Shipping"
	address.country = dataent.get_value("Country", filters={"code":raw_billing_data.get("country", "IN").lower()})
	address.state =  raw_billing_data.get("state")
	address.pincode =  str(raw_billing_data.get("postcode"))
	address.phone = str(raw_billing_data.get("phone"))
	address.email_id = str(raw_billing_data.get("email"))

	address.append("links", {
		"link_doctype": "Customer",
		"link_name": customer.customer_name
	})

	address.save()
	dataent.db.commit()

	if customer_status == 1:

		address = dataent.get_doc("Address",{"woocommerce_email":customer_woo_com_email})
		old_address_title = address.name
		new_address_title = customer.customer_name+"-billing"
		address.address_title = customer.customer_name
		address.save()

		dataent.rename_doc("Address",old_address_title,new_address_title)

	dataent.db.commit()

def link_item(item_data,item_status):
	woocommerce_settings = dataent.get_doc("Woocommerce Settings")

	if item_status == 0:
		#Create Item
		item = dataent.new_doc("Item")

	if item_status == 1:
		#Edit Item
		item_woo_com_id = item_data.get("product_id")
		item = dataent.get_doc("Item",{"woocommerce_id": item_woo_com_id})

	item.item_name = str(item_data.get("name"))
	item.item_code = "woocommerce - " + str(item_data.get("product_id"))
	item.woocommerce_id = str(item_data.get("product_id"))
	item.item_group = _("WooCommerce Products")
	item.stock_uom = woocommerce_settings.uom or _("Nos")
	item.save()
	dataent.db.commit()

def add_tax_details(sales_order,price,desc,status):

	woocommerce_settings = dataent.get_doc("Woocommerce Settings")

	if status == 0:
		# Product taxes
		account_head_type = woocommerce_settings.tax_account

	if status == 1:
		# Shipping taxes
		account_head_type = woocommerce_settings.f_n_f_account

	sales_order.append("taxes",{
							"charge_type":"Actual",
							"account_head": account_head_type,
							"tax_amount": price,
							"description": desc
							})
