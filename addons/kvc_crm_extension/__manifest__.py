{
    'name': 'KaliVibe Coding - CRM Programs & Cohort Tracking',
    'summary': 'Manage Educational Programs, Cohorts, and Student Roster in Odoo CRM',
    'description': '''
        KaliVibe Coding Enterprise Workforce Education Module:
        - Manage Certification Programs & AI Skill Curriculums
        - Track Cohorts with Start/End dates, capacity & instructors
        - Student Roster & CRM Lead Integration
        - Attendance, Certification & Career Placement Status Tracking
    ''',
    'author': 'Rick Jefferson | KaliVibe Coding',
    'website': 'https://kalivibecoding.com',
    'category': 'Sales/CRM',
    'version': '18.0.1.0.0',
    'depends': ['base', 'crm', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/program_views.xml',
        'views/cohort_views.xml',
        'views/student_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
