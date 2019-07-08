from __future__ import unicode_literals
import dataent
from dataent.model.utils.rename_field import rename_field

def execute():
	# 'Schools' module changed to the 'Education'


	dataent.rename_doc("DocType", "Evaluation Criteria", "Assessment Criteria", force=True)
	# dataent.reload_doc("schools", "doctype", "assessment_criteria")
	dataent.reload_doc("education", "doctype", "assessment_criteria")
	if 'evaluation_criteria' in dataent.db.get_table_columns('Assessment Criteria'):
		rename_field("Assessment Criteria", "evaluation_criteria", "assessment_criteria")

	dataent.rename_doc("DocType", "Assessment Evaluation Criteria", "Assessment Plan Criteria", force=True)
	# dataent.reload_doc("schools", "doctype", "assessment_plan_criteria")
	dataent.reload_doc("education", "doctype", "assessment_plan_criteria")
	if 'evaluation_criteria' in dataent.db.get_table_columns('Assessment Plan'):
		rename_field("Assessment Plan Criteria", "evaluation_criteria", "assessment_criteria")

	# dataent.reload_doc("schools", "doctype", "assessment_plan")
	dataent.reload_doc("education", "doctype", "assessment_plan")
	rename_field("Assessment Plan", "evaluation_criterias", "assessment_criteria")

	# dataent.reload_doc("schools", "doctype", "assessment_result_detail")
	dataent.reload_doc("education", "doctype", "assessment_result_detail")
	if 'evaluation_criteria' in dataent.db.get_table_columns('Assessment Result Detail'):
		rename_field("Assessment Result Detail", "evaluation_criteria", "assessment_criteria")

	dataent.rename_doc("DocType", "Course Evaluation Criteria", "Course Assessment Criteria", force=True)
	# dataent.reload_doc("schools", "doctype", "course_assessment_criteria")
	dataent.reload_doc("education", "doctype", "course_assessment_criteria")
	if 'evaluation_criteria' in dataent.db.get_table_columns('Course Assessment Criteria'):
		rename_field("Course Assessment Criteria", "evaluation_criteria", "assessment_criteria")

	# dataent.reload_doc("schools", "doctype", "course")
	dataent.reload_doc("education", "doctype", "course")
	if 'evaluation_criteria' in dataent.db.get_table_columns('Course'):
		rename_field("Course", "evaluation_criterias", "assessment_criteria")
