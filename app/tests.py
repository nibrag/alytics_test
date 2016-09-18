import json
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from model_mommy import mommy
from .models import Data


class IndexViewTestCase(TestCase):
    url = reverse('index')

    def setUp(self):
        self.client = Client()

    def test_get(self):
        mommy.make(Data, _quantity=10)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table', response.content)
        self.assertGreater(response.content.count(b'<tr>'), 10)

    def test_post(self):
        response = self.client.post(
            self.url, data={'name': 'name', 'data': json.dumps({'a': 1})})
        self.assertEqual(response.status_code, 200)

        data = Data.objects.first()
        self.assertIsNotNone(data)
        self.assertEqual(data.name, 'name')
        self.assertDictEqual(data.data, {'a': 1})

    def test_post_invalid_data(self):
        response = self.client.post(
            self.url, data={'name': 'name', 'data': 'bad_data'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Data.objects.exists())
