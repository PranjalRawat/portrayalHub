from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel
from portfolioApi.serializers import UserProfileSerializer
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.views.test_UserProfileViewSet
class UserProfileViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('userprofileInfo-list')
        self.pk = 1
        self.detail_url = reverse('userprofileInfo-detail', kwargs={'pk': self.pk})

        self.user_data = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': fake.password(),
        }
        self.userInstance = User.objects.create_superuser(**self.user_data)

        self.user_profile = {
            'user' : self.userInstance,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(),
            'gender': fake.random_element(elements = ('M', 'F', 'O')),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
        }
        self.userProfileInstance = UserProfileModel.objects.create(**self.user_profile)

    def test_user_profile_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = UserProfileSerializer(UserProfileModel.objects.all(), many=True).data
        view_data = response.data

        self.assertEqual(len(serialized_data), len(view_data))
        self.assertEqual(serialized_data, view_data)

    def test_user_profile_detail_view(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = UserProfileSerializer(UserProfileModel.objects.get(id=self.pk)).data
        view_data = response.data

        self.assertEqual(serialized_data, view_data)

    def test_user_profile_can_have_only_one_instance(self):
        self.client.login(**self.user_data)
        user_profile = {
            'user' : self.userInstance.pk,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(),
            'gender': fake.random_element(elements = ('M', 'F', 'O')),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
        }
        response = self.client.post(self.list_url, user_profile)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cannot_put_data(self):
        self.client.logout()
        user_profile = {
            'user' : self.userInstance.pk,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(),
            'gender': fake.random_element(elements = ('M', 'F', 'O')),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
        }

        response = self.client.patch(self.detail_url, user_profile)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_put_data(self):
        self.client.login(**self.user_data)
        user_profile = {
            'user' : self.userInstance.pk,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(),
            'gender': fake.random_element(elements = ('M', 'F', 'O')),
            'address': fake.address(),
            'email': fake.email(),
        }

        response_list_data_before_patch = self.client.get(self.detail_url).data
        response = self.client.patch(self.detail_url, user_profile)
        response_list_data_after_patch = self.client.get(self.detail_url).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_list_data_before_patch, response_list_data_after_patch)

    def test_unauthorized_user_cannot_patch_data(self):
        self.client.logout()
        user_profile = {
            'user' : self.userInstance.pk,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
        }

        response = self.client.patch(self.detail_url, user_profile)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_patch_data(self):
        self.client.login(**self.user_data)
        user_profile = {
            'user' : self.userInstance.pk,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
        }

        response_list_data_before_patch = self.client.get(self.detail_url).data
        response = self.client.patch(self.detail_url, user_profile)
        response_list_data_after_patch = self.client.get(self.detail_url).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_list_data_before_patch, response_list_data_after_patch)

    def test_unauthorized_user_cannot_delete_data(self):
        self.client.logout()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_delete_data(self):
        self.client.login(**self.user_data)
        response_list_data_before_delete = self.client.get(self.list_url).data
        response_delete = self.client.delete(self.detail_url)
        response_list_data_after_delete = self.client.get(self.list_url).data

        # Assert list data is deleted
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response_list_data_before_delete), len(response_list_data_after_delete) + 1)
