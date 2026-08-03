{
    'name': 'KaliVibe Coding - Odoo Brand & Dark Theme',
    'summary': 'Enterprise Brand & Dark Theme Customization for KaliVibe Coding',
    'description': 'Custom branding module for Odoo ERP/CRM for KaliVibe Coding workforce education.',
    'author': 'Rick Jefferson | KaliVibe Coding',
    'website': 'https://kalivibecoding.com',
    'category': 'Themes/Backend',
    'version': '18.0.1.0.0',
    'depends': ['web'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kvc_theme/static/src/scss/kvc_backend.scss',
        ],
        'web.assets_frontend': [
            'kvc_theme/static/src/scss/kvc_frontend.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
