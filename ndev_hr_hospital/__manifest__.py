{
    'name': "HR Hospital",
    'version': '16.0.1.0.4',
    'category': 'Human Resources/Employees',

    'summary': """
        Odoo School
        Practise 2""",

    'author': "Svyatoslav Nadozirny",
    'website': "https://www.yourcompany.com",
    'maintainer': 'NDev',
    'depends': ['portal', 'mail'],
    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_contact_person_views.xml',
        'views/hospital_disease_views.xml',
        'views/hospital_diagnose_views.xml',
        'views/hospital_visit_views.xml',
        'views/hospital_analysis_views.xml',
        'views/hospital_menus.xml',
        'data/disease_data.xml',
        'data/visits_sequence.xml',
        'wizard/choose_diagnose_views.xml',
        'wizard/select_doctor_views.xml',
        'wizard/doctor_visit_views.xml',
        'report/doctor_visit_report.xml',
        'report/doctor_report.xml',

    ],
    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3'
}
