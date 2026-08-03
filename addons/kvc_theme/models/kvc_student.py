# -*- coding: utf-8 -*-
"""KVC Student — enrollment record linking a partner to a cohort."""

from odoo import models, fields, api


class KvcStudent(models.Model):
    _name = 'kvc.student'
    _description = 'KVC Student Enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'enrollment_date desc'

    # ── Core links ───────────────────────────────────────────────
    partner_id = fields.Many2one(
        'res.partner', string='Student',
        required=True, ondelete='restrict', tracking=True,
    )
    cohort_id = fields.Many2one(
        'kvc.cohort', string='Cohort',
        required=True, ondelete='cascade', tracking=True,
    )
    program_id = fields.Many2one(
        related='cohort_id.program_id',
        string='Program', store=True, readonly=True,
    )

    # ── Status ──────────────────────────────────────────────────
    state = fields.Selection([
        ('inquiry', 'Inquiry'),
        ('applied', 'Applied'),
        ('enrolled', 'Enrolled'),
        ('active', 'Active — In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('cancelled', 'Cancelled'),
    ], string='Enrollment Status', default='inquiry', tracking=True)

    enrollment_date = fields.Date(
        string='Enrollment Date',
        default=fields.Date.today,
        tracking=True,
    )
    completion_date = fields.Date(string='Completion Date', tracking=True)

    # ── Funding ─────────────────────────────────────────────────
    funding_source = fields.Selection(
        related='program_id.funding_source',
        string='Funding Source', store=True, readonly=True,
    )
    scholarship_amount = fields.Monetary(
        string='Scholarship Amount',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
    )
    payment_status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid in Full'),
        ('waived', 'Waived / Scholarship'),
        ('invoiced', 'Invoiced'),
    ], string='Payment Status', default='unpaid', tracking=True)
    stripe_customer_id = fields.Char(string='Stripe Customer ID')

    # ── Progress ────────────────────────────────────────────────
    progress_pct = fields.Float(
        string='Progress (%)',
        default=0.0,
        digits=(5, 1),
    )
    grade = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('incomplete', 'Incomplete'),
        ('pending', 'Pending'),
    ], string='Final Grade', default='pending')
    certificate_issued = fields.Boolean(string='Certificate Issued', default=False)
    certificate_date = fields.Date(string='Certificate Date')

    # ── GHL sync ────────────────────────────────────────────────
    ghl_contact_id = fields.Char(string='GHL Contact ID')
    ghl_opportunity_id = fields.Char(string='GHL Opportunity ID')

    # ── Notes ───────────────────────────────────────────────────
    notes = fields.Text(string='Notes')

    # ── Computed display ────────────────────────────────────────
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
    )

    @api.depends('partner_id', 'cohort_id')
    def _compute_display_name(self):
        for rec in self:
            partner = rec.partner_id.name or ''
            cohort = rec.cohort_id.name or ''
            rec.display_name = f'{partner} — {cohort}' if cohort else partner

    def action_enroll(self):
        self.write({'state': 'enrolled'})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        self.write({
            'state': 'completed',
            'completion_date': fields.Date.today(),
            'progress_pct': 100.0,
        })

    def action_issue_certificate(self):
        self.write({
            'certificate_issued': True,
            'certificate_date': fields.Date.today(),
        })

    def action_drop(self):
        self.write({'state': 'dropped'})
