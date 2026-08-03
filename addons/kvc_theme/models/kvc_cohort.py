# -*- coding: utf-8 -*-
"""KVC Cohort — a scheduled run of a KVC Program with enrolled students."""

from odoo import models, fields, api


class KvcCohort(models.Model):
    _name = 'kvc.cohort'
    _description = 'KVC Program Cohort'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(string='Cohort Name', required=True, tracking=True)
    program_id = fields.Many2one(
        'kvc.program', string='Program',
        required=True, ondelete='cascade', tracking=True,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Enrollment Open'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    instructor_id = fields.Many2one('res.users', string='Lead Instructor')

    student_ids = fields.One2many(
        'kvc.student', 'cohort_id',
        string='Students',
    )
    student_count = fields.Integer(
        string='Enrolled',
        compute='_compute_student_count',
        store=True,
    )
    seats_remaining = fields.Integer(
        string='Seats Remaining',
        compute='_compute_student_count',
        store=True,
    )

    meeting_link = fields.Char(string='Meeting Link (Zoom/Meet)')
    notes = fields.Text(string='Internal Notes')

    @api.depends('student_ids', 'program_id.max_students')
    def _compute_student_count(self):
        for rec in self:
            enrolled = len(rec.student_ids.filtered(lambda s: s.state not in ('dropped', 'cancelled')))
            rec.student_count = enrolled
            max_s = rec.program_id.max_students or 0
            rec.seats_remaining = max(0, max_s - enrolled)

    def action_open(self):
        self.write({'state': 'open'})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
