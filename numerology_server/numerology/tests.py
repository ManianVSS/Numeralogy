from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import NameEntry


class NumerologyTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_name_entry_creation(self):
        entry = NameEntry.objects.create(name='Alice')
        self.assertEqual(entry.sum, 1 + 3 + 1 + 3 + 5)
        self.assertEqual(entry.recursive_sum, 4)

    def test_upload_api_accepts_text_file(self):
        url = reverse('numerology:upload-api')
        content = 'Alice\nBob\n'
        uploaded_file = SimpleUploadedFile('names.txt', content.encode('utf-8'), content_type='text/plain')
        response = self.client.post(url, {'file': uploaded_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NameEntry.objects.count(), 2)

    def test_upload_form_view(self):
        url = reverse('numerology:upload')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Dictionary file')
