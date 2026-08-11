from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import NameEntry


class NumerologyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_name_entry_creation(self):
        entry = NameEntry.objects.create(name='Alice', initial='A')
        self.assertEqual(entry.full_name, 'Alice A')
        self.assertEqual(entry.sum_without_initial, 1 + 3 + 1 + 3 + 5)
        self.assertEqual(entry.recursive_sum_without_initial, 4)
        self.assertEqual(entry.sum, 1 + 3 + 1 + 3 + 5 + 1)
        self.assertEqual(entry.recursive_sum, 5)

    def test_upload_api_accepts_text_file(self):
        url = reverse('numerology:upload-api')
        content = 'Alice\nBob\n'
        response = self.client.post(url, {'file': ('names.txt', content, 'text/plain')}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NameEntry.objects.count(), 2)

    def test_upload_form_view(self):
        url = reverse('numerology:upload')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Dictionary file')
