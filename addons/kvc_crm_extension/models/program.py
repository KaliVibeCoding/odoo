# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KvcProgram(models.Model):
    _name = 'kvc.program'
    _description = 'KaliVibe Coding Workforce Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Program Name', required=True, tracking=True)
    code = fields.Char(string='Program Code', required=True)
    description = fields.Text(string='Syllabus & Overview')
    duration_weeks = fields.Integer(string='Duration (Weeks)', default=8, required=True)
    tuition_fee = fields.Float(string='Tuition Fee ($)', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    
    level = fields.Selection([
        ('beginner', 'Beginner / AI Foundations'),
        ('intermediate', 'Intermediate / Full-Stack Agentic'),
        ('advanced', 'Advanced / Supreme AGI Architect')
    ], string='Level', default='intermediate', required=True)

    cohort_ids = fields.One2many('kvc.cohort', 'program_id', string='Cohorts')
    total_cohorts = fields.Integer(string='Total Cohorts', compute='_compute_totals')
    total_students = fields.Integer(string='Total Students Enrolled', compute='_compute_totals')

    @api.depends('cohort_ids', 'cohort_ids.student_ids')
    def _compute_totals(self):
        for record in self:
            record.total_cohorts = len(record.cohort_ids)
            record.total_students = sum(len(c.student_ids) for c in record.cohort_ids)
