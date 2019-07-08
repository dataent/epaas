# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import dataent
from dataent import _
from dataent.model.document import Document
from dataent.contacts.address_and_contact import load_address_and_contact, delete_contact_and_address

class BankAccount(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def autoname(self):
		self.name = self.account_name + " - " + self.bank

	def on_trash(self):
		delete_contact_and_address('BankAccount', self.name)

	def validate(self):
		self.validate_company()
		self.validate_iban()

	def validate_company(self):
		if self.is_company_account and not self.company:
			dataent.throw(_("Company is manadatory for company account"))

	def validate_iban(self):
		'''
		Algorithm: https://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN
		'''
		# IBAN field is optional
		if not self.iban:
			return

		def encode_char(c):
			# Position in the alphabet (A=1, B=2, ...) plus nine
			return str(9 + ord(c) - 64)

		# remove whitespaces, upper case to get the right number from ord()
		iban = ''.join(self.iban.split(' ')).upper()

		# Move country code and checksum from the start to the end
		flipped = iban[4:] + iban[:4]

		# Encode characters as numbers
		encoded = [encode_char(c) if ord(c) >= 65 and ord(c) <= 90 else c for c in flipped]

		to_check = int(''.join(encoded))

		if to_check % 97 != 1:
			dataent.throw(_('IBAN is not valid'))


@dataent.whitelist()
def make_bank_account(doctype, docname):
	doc = dataent.new_doc("Bank Account")
	doc.party_type = doctype
	doc.party = docname
	doc.is_default = 1

	return doc

@dataent.whitelist()
def get_party_bank_account(party_type, party):
	return dataent.db.get_value(party_type,
		party, 'default_bank_account')

@dataent.whitelist()
def get_bank_account_details(bank_account):
	return dataent.db.get_value("Bank Account",
		bank_account, ['account', 'bank', 'bank_account_no'], as_dict=1)
