from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_simple(self):

        data = {
            'type': 'SIMPLE',
            'seats':7,
            'options': [
                { 'option': 'Mortadelo', 'number': 1, 'votes': 5 }, #2.285
                { 'option': 'Filemon', 'number': 2, 'votes': 0 },
                { 'option': 'Bacterio', 'number': 3, 'votes': 3 },
                { 'option': 'Ofelia', 'number': 4, 'votes': 2 },
                { 'option': 'Super', 'number': 5, 'votes': 5 },
                { 'option': 'Botones Sacarino', 'number': 6, 'votes': 1 },
        
            ]
        }

        expected_result = [
            { 'option': 'Mortadelo', 'number': 1, 'votes': 5, 'postproc': 2 },#0.188
            { 'option': 'Super', 'number': 5, 'votes': 5, 'postproc': 2 },#0.188
            { 'option': 'Bacterio', 'number': 3, 'votes': 3, 'postproc': 1 },#0.31
            { 'option': 'Ofelia', 'number': 4, 'votes': 2, 'postproc': 1 },#0.14
            { 'option': 'Botones Sacarino', 'number': 6, 'votes': 1, 'postproc': 1 },#0.285
            { 'option': 'Filemon', 'number': 2, 'votes': 0, 'postproc': 0 },

        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)