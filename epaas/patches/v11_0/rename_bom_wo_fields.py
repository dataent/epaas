# Copyright (c) 2018, Dataent and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
    for doctype in ['BOM Explosion Item', 'BOM Item', 'Work Order Item', 'Item']:
        if dataent.db.has_column(doctype, 'allow_transfer_for_manufacture'):
            if doctype != 'Item':
                dataent.reload_doc('manufacturing', 'doctype', dataent.scrub(doctype))
            else:
                dataent.reload_doc('stock', 'doctype', dataent.scrub(doctype))

            rename_field(doctype, "allow_transfer_for_manufacture", "include_item_in_manufacturing")

    if dataent.db.has_column('BOM', 'allow_same_item_multiple_times'):
        dataent.db.sql(""" UPDATE tabBOM
            SET
                allow_same_item_multiple_times = 0
            WHERE
                trim(coalesce(allow_same_item_multiple_times, '')) = '' """)

    for doctype in ['BOM', 'Work Order']:
        dataent.reload_doc('manufacturing', 'doctype', dataent.scrub(doctype))

        if dataent.db.has_column(doctype, 'transfer_material_against_job_card'):
            dataent.db.sql(""" UPDATE `tab%s`
                SET transfer_material_against = CASE WHEN
                    transfer_material_against_job_card = 1 then 'Job Card' Else 'Work Order' END
                WHERE docstatus < 2""" % (doctype))
        else:
            dataent.db.sql(""" UPDATE `tab%s`
                SET transfer_material_against = 'Work Order'
                WHERE docstatus < 2""" % (doctype))