# -*- coding: utf-8 -*-
{
    'name': "asset",

    'summary': """
        Assets for tickets""",

    'description': """
        Asset management
    """,

    'author': "Svyatoslav Nadozirny",
    'website': "https://ndev.online",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_model_views.xml',
        'views/asset_asset_views.xml',
        'views/asset_menus.xml',
        'data/asset_data.xml',
    ],
}
