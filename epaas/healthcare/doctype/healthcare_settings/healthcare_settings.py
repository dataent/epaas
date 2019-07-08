# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document
from dataent.core.doctype.sms_settings.sms_settings import send_sms
import json

class HealthcareSettings(Document):
	def validate(self):
		for key in ["collect_registration_fee","manage_customer","patient_master_name",
		"require_test_result_approval","require_sample_collection", "default_medical_code_standard"]:
			dataent.db.set_default(key, self.get(key, ""))
		if(self.collect_registration_fee):
			if self.registration_fee <= 0 :
				dataent.throw(_("Registration fee can not be Zero"))
		if self.inpatient_visit_charge_item:
			validate_service_item(self.inpatient_visit_charge_item, "Configure a service Item for Inpatient Visit Charge Item")
		if self.op_consulting_charge_item:
			validate_service_item(self.op_consulting_charge_item, "Configure a service Item for Out Patient Consulting Charge Item")
		if self.clinical_procedure_consumable_item:
			validate_service_item(self.clinical_procedure_consumable_item, "Configure a service Item for Clinical Procedure Consumable Item")

@dataent.whitelist()
def get_sms_text(doc):
    sms_text = {}
    doc = dataent.get_doc("Lab Test",doc)
    #doc = json.loads(doc)
    context = {"doc": doc, "alert": doc, "comments": None}
    emailed = dataent.db.get_value("Healthcare Settings", None, "sms_emailed")
    sms_text['emailed'] = dataent.render_template(emailed, context)
    printed = dataent.db.get_value("Healthcare Settings", None, "sms_printed")
    sms_text['printed'] = dataent.render_template(printed, context)
    return sms_text

def send_registration_sms(doc):
    if (dataent.db.get_value("Healthcare Settings", None, "reg_sms")=='1'):
        if doc.mobile:
            context = {"doc": doc, "alert": doc, "comments": None}
            if doc.get("_comments"):
                context["comments"] = json.loads(doc.get("_comments"))
            messages = dataent.db.get_value("Healthcare Settings", None, "reg_msg")
            messages = dataent.render_template(messages, context)
            number = [doc.mobile]
            send_sms(number,messages)
        else:
            dataent.msgprint(doc.name + " Has no mobile number to send registration SMS", alert=True)


def get_receivable_account(company):
    receivable_account = get_account(None, "receivable_account", "Healthcare Settings", company)
    if receivable_account:
        return receivable_account
    return dataent.get_cached_value('Company',  company,  "default_receivable_account")

def get_income_account(practitioner, company):
    if(practitioner):
        income_account = get_account("Healthcare Practitioner", None, practitioner, company)
        if income_account:
            return income_account
    income_account = get_account(None, "income_account", "Healthcare Settings", company)
    if income_account:
        return income_account
    return dataent.get_cached_value('Company',  company,  "default_income_account")

def get_account(parent_type, parent_field, parent, company):
    if(parent_type):
        return dataent.db.get_value("Party Account",
            {"parenttype": parent_type, "parent": parent, "company": company}, "account")
    if(parent_field):
        return dataent.db.get_value("Party Account",
            {"parentfield": parent_field, "parent": parent, "company": company}, "account")

def validate_service_item(item, msg):
	if dataent.db.get_value("Item", item, "is_stock_item") == 1:
		dataent.throw(_(msg))
