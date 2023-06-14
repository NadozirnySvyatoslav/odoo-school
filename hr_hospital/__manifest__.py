{
    'name': "HR Hospital",
    'version': '1.0.0.0.1',
    'category': 'Human Resources/Employees',

    'summary': """
        Odoo School
        Practise 2""",

    'author': "Svyatoslav Nadozirny",
    'website': "https://www.yourcompany.com",
    'maintainer': 'NDev',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_doctor_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_menus.xml',
        'data/disease_data.xml',
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
