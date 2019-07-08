# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.utils.nestedset import get_root_of
from dataent.model.document import Document
from six.moves.urllib.parse import urlparse

class WoocommerceSettings(Document):
	def validate(self):
		self.validate_settings()
		self.create_delete_custom_fields()
		self.create_webhook_url()

	def create_delete_custom_fields(self):
		if self.enable_sync:
			# create
			create_custom_field_id_and_check_status = False
			create_custom_field_email_check = False
			names = ["Customer-woocommerce_id","Sales Order-woocommerce_id","Item-woocommerce_id","Address-woocommerce_id"]
			names_check_box = ["Customer-woocommerce_check","Sales Order-woocommerce_check","Item-woocommerce_check","Address-woocommerce_check"]
			email_names = ["Customer-woocommerce_email","Address-woocommerce_email"]

			for i in zip(names,names_check_box):

				if not dataent.get_value("Custom Field",{"name":i[0]}) or not dataent.get_value("Custom Field",{"name":i[1]}):
					create_custom_field_id_and_check_status = True
					break


			if create_custom_field_id_and_check_status:
				names = ["Customer","Sales Order","Item","Address"]
				for name in names:
					custom = dataent.new_doc("Custom Field")
					custom.dt = name
					custom.label = "woocommerce_id"
					custom.read_only = 1
					custom.save()

					custom = dataent.new_doc("Custom Field")
					custom.dt = name
					custom.label = "woocommerce_check"
					custom.fieldtype = "Check"
					custom.read_only = 1
					custom.save()

			for i in email_names:

				if not dataent.get_value("Custom Field",{"name":i}):
					create_custom_field_email_check = True
					break;

			if create_custom_field_email_check:
				names = ["Customer","Address"]
				for name in names:
					custom = dataent.new_doc("Custom Field")
					custom.dt = name
					custom.label = "woocommerce_email"
					custom.read_only = 1
					custom.save()

			if not dataent.get_value("Item Group",{"name": _("WooCommerce Products")}):
				item_group = dataent.new_doc("Item Group")
				item_group.item_group_name = _("WooCommerce Products")
				item_group.parent_item_group = get_root_of("Item Group")
				item_group.save()


		elif not self.enable_sync:
			# delete
			names = ["Customer-woocommerce_id","Sales Order-woocommerce_id","Item-woocommerce_id","Address-woocommerce_id"]
			names_check_box = ["Customer-woocommerce_check","Sales Order-woocommerce_check","Item-woocommerce_check","Address-woocommerce_check"]
			email_names = ["Customer-woocommerce_email","Address-woocommerce_email"]
			for name in names:
				dataent.delete_doc("Custom Field",name)

			for name in names_check_box:
				dataent.delete_doc("Custom Field",name)

			for name in email_names:
				dataent.delete_doc("Custom Field",name)

			dataent.delete_doc("Item Group", _("WooCommerce Products"))

		dataent.db.commit()

	def validate_settings(self):
		if self.enable_sync:
			if not self.secret:
				self.set("secret", dataent.generate_hash())

			if not self.woocommerce_server_url:
				dataent.throw(_("Please enter Woocommerce Server URL"))

			if not self.api_consumer_key:
				dataent.throw(_("Please enter API Consumer Key"))

			if not self.api_consumer_secret:
				dataent.throw(_("Please enter API Consumer Secret"))

	def create_webhook_url(self):
		endpoint = "/api/method/epaas.epaas_integrations.connectors.woocommerce_connection.order"

		try:
			url = dataent.request.url
		except RuntimeError:
			# for CI Test to work
			url = "http://localhost:8000"

		server_url = '{uri.scheme}://{uri.netloc}'.format(
			uri=urlparse(url)
		)

		delivery_url = server_url + endpoint
		self.endpoint = delivery_url

@dataent.whitelist()
def generate_secret():
	woocommerce_settings = dataent.get_doc("Woocommerce Settings")
	woocommerce_settings.secret = dataent.generate_hash()
	woocommerce_settings.save()

@dataent.whitelist()
def get_series():
	return {
		"sales_order_series" : dataent.get_meta("Sales Order").get_options("naming_series") or "SO-WOO-",
	}