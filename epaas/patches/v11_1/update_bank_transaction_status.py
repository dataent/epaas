# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
    dataent.reload_doc("accounts", "doctype", "bank_transaction")

    dataent.db.sql(""" UPDATE `tabBank Transaction`
        SET status = 'Reconciled'
        WHERE
            status = 'Settled' and (debit = allocated_amount or credit = allocated_amount)
            and ifnull(allocated_amount, 0) > 0
    """)