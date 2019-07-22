from django.test import TestCase
from django.urls import reverse
# Create your tests here.

class RegisterTest(TestCase):
    def test_register_view_status_code(self):
        url = reverse('user:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)