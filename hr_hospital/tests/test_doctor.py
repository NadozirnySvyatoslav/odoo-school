from odoo.tests.common import TransactionCase

class TestDoctor(TransactionCase):
    def setUp(self):
        super(TestDoctor, self).setUp()

        self.doctor=self.env['hr_hospital'].create({
            'first_name': "Who",
            'surname': "Doctor",
            'sex': 'male',
            'birthday': '2000-01-01',
        })

