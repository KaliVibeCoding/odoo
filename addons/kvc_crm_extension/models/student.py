# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KvcStudent(models.Model):
    _name = 'kvc.student'
    _description = 'KaliVibe Coding Student Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string='Contact / Lead', required=True, ondelete='cascade')
    name = fields.Char(related='partner_id.name', string='Student Name', store=True)
    email = fields.Char(related='partner_id.email', string='Email', store=True)
    phone = fields.Char(related='partner_id.phone', string='Phone', store=True)

    program_id = fields.Many2one('kvc.program', string='Program', required=True)
    cohort_id = fields.Many2one('kvc.cohort', string='Cohort', domain="[('program_id', '=', program_id)]")
    
    crm_lead_id = fields.Many2one('crm.lead', string='Associated CRM Lead')

    progress_percentage = fields.Float(string='Course Progress (%)', default=0.0)
    attendance_rate = fields.Float(string='Attendance Rate (%)', default=100.0)

    certification_status = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('certified', 'Certified / Graduated'),
        ('failed', 'Incomplete')
    ], string='Certification Status', default='in_progress', tracking=True)

    career_placement_status = fields.Selection([
        ('seeking', 'Seeking Placement'),
        ('placed', 'Placed in AI/Tech Role'),
        ('entrepreneur', 'Launched Own AI Agency/Business'),
        ('not_applicable', 'N/A')
    ], string='Career Placement Status', default='seeking', tracking=True)

    notes = fields.Text(string='Student Notes & Evaluation')
