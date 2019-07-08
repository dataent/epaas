# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent

def execute():
	dataent.db.sql("""update `tabStock Entry` set purpose='Manufacture' where purpose='Manufacture/Repack' and ifnull(work_order,"")!="" """)
	dataent.db.sql("""update `tabStock Entry` set purpose='Repack' where purpose='Manufacture/Repack' and ifnull(work_order,"")="" """)