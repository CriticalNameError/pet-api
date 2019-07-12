from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Pets

from pet_logic.serializers import PetsSerializer


PETS_URL = reverse('pet_logic:pets-list')


# Some helper functions

def sample_pet(id=1):
    """Return a sample pet"""
    return Pets.objects.get(id=id)

def detail_url(pet_id):
    """Return details url"""
    return reverse('pet_logic:pets-detail', args=[pet_id])



class PetsApiTests(TestCase):
    """Test pets API functionality"""

    def setUp(self):
        self.client = APIClient()
        Pets.objects.create(id=1,name='Dog', species='Dog', gender='m', birthday='2015-01-01')

    def test_listing_pets(self):
        """Test GET Request for retreiving list of pets"""
        res = self.client.get(PETS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_partial_update_pets(self):
        """Test updating a pet with patch"""
        pet = sample_pet(id=1)

        payload = {'name': 'Fox', 'gender': 'w'}
        url = detail_url(pet.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        pet.refresh_from_db()
        self.assertIn(pet.name, payload['name'])
        self.assertIn(pet.gender, payload['gender'])


