# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
    for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
        if dataent.db.exists("Report", report):
            dataent.delete_doc("Report", report)