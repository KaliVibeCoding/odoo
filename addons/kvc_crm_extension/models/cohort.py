# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KvcCohort(models.Model):
    _name = 'kvc.cohort'
    _description = 'KaliVibe Coding Student Cohort'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Cohort Name', required=True, tracking=True)
    program_id = fields.Many2one('kvc.program', string='Program', required=True, ondelete='cascade')
    instructor_id = fields.Many2one('res.users', string='Lead Instructor', default=lambda self: self.env.user)
    
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    max_capacity = fields.Integer(string='Max Capacity', default=25, required=True)
    
    state = fields.Selection([
        ('draft', 'Draft / Enrolling'),
        ('active', 'Active In-Session'),
        ('completed', 'Completed / Graduated'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    student_ids = fields.One2many('kvc.student', 'cohort_id', string='Enrolled Students')
    enrolled_count = fields.Integer(string='Enrolled Count', compute='_compute_enrolled')

    @api.depends('student_ids')
    def _compute_enrolled(self):
        for record in self:
            record.enrolled_count = len(record.student_ids)
