# -*- coding: utf-8 -*-
"""
KVC Program model — tracks KaliVibeCoding training programs.
WIOA Title I / Perkins V / NAICS 611420, 611430, 541512, 541715 aligned.
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KvcProgram(models.Model):
    _name = 'kvc.program'
    _description = 'KVC Training Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, name'

    # ── Identity ────────────────────────────────────────────────
    name = fields.Char(
        string='Program Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Program Code',
        size=20,
        copy=False,
        readonly=True,
        default='New',
    )
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color Index', default=0)

    # ── Classification ──────────────────────────────────────────
    program_type = fields.Selection([
        ('bootcamp', 'Coding Bootcamp'),
        ('workshop', 'Workshop / Short Course'),
        ('apprenticeship', 'Apprenticeship'),
        ('certificate', 'Certificate Program'),
        ('mentorship', 'Mentorship Track'),
        ('government', 'Government Contract Program'),
    ], string='Program Type', required=True, default='bootcamp', tracking=True)

    funding_source = fields.Selection([
        ('private', 'Private / Self-Pay'),
        ('wioa_i', 'WIOA Title I'),
        ('wioa_iii', 'WIOA Title III'),
        ('perkins_v', 'Perkins V'),
        ('grant', 'Grant Funded'),
        ('government_contract', 'Government Contract'),
        ('scholarship', 'Scholarship'),
    ], string='Funding Source', default='private', tracking=True)

    naics_code = fields.Selection([
        ('611420', '611420 — Computer Training'),
        ('611430', '611430 — Professional & Mgmt Dev'),
        ('541512', '541512 — Computer Systems Design'),
        ('541715', '541715 — R&D in Computer Science'),
    ], string='NAICS Code', default='611420')

    # ── Schedule ────────────────────────────────────────────────
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    duration_weeks = fields.Integer(
        string='Duration (weeks)',
        compute='_compute_duration',
        store=True,
    )
    schedule_notes = fields.Text(string='Schedule Notes')

    # ── Capacity ────────────────────────────────────────────────
    max_students = fields.Integer(string='Max Students', default=20)
    cohort_ids = fields.One2many(
        'kvc.cohort', 'program_id',
        string='Cohorts',
    )
    cohort_count = fields.Integer(
        string='Cohort Count',
        compute='_compute_cohort_count',
        store=True,
    )

    # ── Financials ──────────────────────────────────────────────
    price = fields.Monetary(string='Program Price', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
    )
    stripe_price_id = fields.Char(string='Stripe Price ID')

    # ── Content ─────────────────────────────────────────────────
    description = fields.Html(string='Program Description')
    outcomes = fields.Text(string='Learning Outcomes')
    prerequisites = fields.Text(string='Prerequisites')
    tech_stack = fields.Char(string='Tech Stack', help='Comma-separated: Next.js, Python, Cloudflare...')

    # ── GoHighLevel sync ────────────────────────────────────────
    ghl_pipeline_id = fields.Char(string='GHL Pipeline ID')
    ghl_stage_id = fields.Char(string='GHL Stage ID')

    # ── Computed ────────────────────────────────────────────────
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                delta = rec.end_date - rec.start_date
                rec.duration_weeks = max(0, delta.days // 7)
            else:
                rec.duration_weeks = 0

    @api.depends('cohort_ids')
    def _compute_cohort_count(self):
        for rec in self:
            rec.cohort_count = len(rec.cohort_ids)

    # ── Sequence ────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('kvc.program') or 'KVC-000'
        return super().create(vals_list)

    # ── Constraints ─────────────────────────────────────────────
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError('End date must be after start date.')

    def name_get(self):
        result = []
        for rec in self:
            name = f'[{rec.code}] {rec.name}' if rec.code and rec.code != 'New' else rec.name
            result.append((rec.id, name))
        return result
