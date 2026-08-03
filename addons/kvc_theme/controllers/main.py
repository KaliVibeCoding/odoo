# -*- coding: utf-8 -*-
"""
KVC Controllers:
  /kvc/webhook/ghl  — GoHighLevel contact sync webhook
  /kvc/portal/*     — Student portal endpoints
"""

import json
import logging
import hmac
import hashlib

from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class KvcGhlWebhook(http.Controller):
    """Receive GoHighLevel webhooks and sync contacts → kvc.student."""

    @http.route('/kvc/webhook/ghl', type='json', auth='public', methods=['POST'], csrf=False)
    def ghl_webhook(self, **kwargs):
        body = request.httprequest.get_data(as_text=True)
        sig = request.httprequest.headers.get('X-GHL-Signature', '')

        # Verify HMAC-SHA256 signature
        secret = request.env['ir.config_parameter'].sudo().get_param('kvc.ghl_webhook_secret', '')
        if secret:
            expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, expected):
                _logger.warning('KVC GHL webhook: invalid signature')
                return Response(status=401)

        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            return Response(status=400)

        event_type = payload.get('type', '')
        contact = payload.get('contact', {})
        ghl_id = contact.get('id', '')

        if not ghl_id:
            return {'status': 'ignored', 'reason': 'no contact id'}

        if event_type in ('ContactCreate', 'ContactUpdate'):
            self._upsert_contact(contact, ghl_id)
        elif event_type == 'OpportunityCreate':
            self._handle_opportunity(payload, ghl_id)

        return {'status': 'ok'}

    def _upsert_contact(self, contact: dict, ghl_id: str):
        Partner = request.env['res.partner'].sudo()
        email = contact.get('email', '')
        name = contact.get('name') or contact.get('full_name') or email or ghl_id
        phone = contact.get('phone', '')

        partner = Partner.search([('email', '=', email)], limit=1) if email else None
        if not partner:
            partner = Partner.search([('phone', '=', phone)], limit=1) if phone else None

        vals = {
            'name': name,
            'email': email,
            'phone': phone,
            'comment': f'GHL Contact ID: {ghl_id}',
        }

        if partner:
            partner.write(vals)
        else:
            partner = Partner.create(vals)

        # Sync ghl_contact_id on any matching student record
        students = request.env['kvc.student'].sudo().search([('partner_id', '=', partner.id)])
        students.write({'ghl_contact_id': ghl_id})
        _logger.info('KVC GHL: upserted partner %s (GHL %s)', partner.id, ghl_id)

    def _handle_opportunity(self, payload: dict, ghl_contact_id: str):
        opp = payload.get('opportunity', {})
        opp_id = opp.get('id', '')
        students = request.env['kvc.student'].sudo().search([('ghl_contact_id', '=', ghl_contact_id)])
        if students:
            students.write({'ghl_opportunity_id': opp_id})
            _logger.info('KVC GHL: linked opportunity %s to %d student(s)', opp_id, len(students))


class KvcPortal(http.Controller):
    """Student-facing portal pages."""

    @http.route('/kvc/portal/dashboard', type='http', auth='user', website=True)
    def student_dashboard(self, **kwargs):
        partner = request.env.user.partner_id
        enrollments = request.env['kvc.student'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', 'not in', ['cancelled']),
        ], order='enrollment_date desc')

        return request.render('kvc_theme.portal_student_dashboard', {
            'enrollments': enrollments,
            'page_name': 'kvc_dashboard',
        })

    @http.route('/kvc/portal/enrollment/<int:enrollment_id>', type='http', auth='user', website=True)
    def enrollment_detail(self, enrollment_id, **kwargs):
        partner = request.env.user.partner_id
        enrollment = request.env['kvc.student'].sudo().browse(enrollment_id)

        if not enrollment.exists() or enrollment.partner_id.id != partner.id:
            return request.not_found()

        return request.render('kvc_theme.portal_enrollment_detail', {
            'enrollment': enrollment,
            'page_name': 'kvc_enrollment',
        })

    @http.route('/kvc/health', type='json', auth='public', methods=['GET'])
    def health(self, **kwargs):
        return {'status': 'ok', 'module': 'kvc_theme'}
