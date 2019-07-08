# Copyright (c) 2015, Dataent Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
    dataent.reload_doc('projects', 'doctype', 'project')

    if dataent.db.has_column('Project', 'from'):
        rename_field('Project', 'from', 'from_time')
        rename_field('Project', 'to', 'to_time')