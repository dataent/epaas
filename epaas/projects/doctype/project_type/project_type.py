# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dataent Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataent.model.document import Document
import dataent
from dataent import _

class ProjectType(Document):
	def on_trash(self):
		if self.name == "External":
			dataent.throw(_("You cannot delete Project Type 'External'"))