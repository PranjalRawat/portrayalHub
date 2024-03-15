from django.conf import settings
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from portfolioApi.models import ProfileImageModel, UserProfileModel
from portfolioApi.serializers import UserProfileImageSerializer
from faker import Faker
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.views.test_ProfileImageViewSet
class ProfileImageViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.media_fields = ['image']
        self.list_url = reverse('userprofileImage-list')
        self.pk = 1
        self.detail_url = reverse('userprofileImage-detail', kwargs={'pk': self.pk})

        # Create a fake image using PIL
        image = Image.new('RGB', (100, 100))  # You can specify the size of the image as needed

        # Convert the image to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        self.upload_dir = 'profile_images'
        self.image_name = 'test_image.jpg'
        # Create a SimpleUploadedFile object from the image bytes
        self.image_file = SimpleUploadedFile(self.image_name, image_bytes.getvalue(), content_type='image/jpeg')

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

        self.profile_image = {
            'user_profile': self.userProfileInstance,
            'image': fake.image_url(),
        }
        ProfileImageModel.objects.create(**self.profile_image)

    def tearDown(self):
        super().tearDown()
        # Delete the created image file from the media directory
        image_file_path = os.path.join(settings.MEDIA_ROOT, self.upload_dir, self.image_name)
        if os.path.exists(image_file_path):
            os.remove(image_file_path)

    def test_user_profile_image_list_view(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = UserProfileImageSerializer(ProfileImageModel.objects.all(), many=True).data[0]
        view_data = response.data[0]

        self.assertEqual(len(serialized_data), len(view_data))
        for key in view_data:
            if key in self.media_fields:
                self.assertIn(serialized_data[key], view_data[key])
            else:
                self.assertEqual(serialized_data[key], view_data[key])

    def test_user_profile_image_detail_view(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = UserProfileImageSerializer(ProfileImageModel.objects.get(id=self.pk)).data
        view_data = response.data

        for key in view_data:
            if key in self.media_fields:
                self.assertIn(serialized_data[key], view_data[key])
            else:
                self.assertEqual(serialized_data[key], view_data[key])

    def test_user_profile_image_can_have_only_one_instance(self):
        self.client.login(**self.user_data)
        profile_image = {
            'user_profile': self.userProfileInstance.pk,
            'image': self.image_file,
        }
        response = self.client.post(self.list_url, profile_image)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cannot_put_data(self):
        self.client.logout()
        profile_image = {
            'user_profile': self.userProfileInstance.pk,
            'image': self.image_file,
        }

        response = self.client.put(self.detail_url, profile_image)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_put_data(self):
        self.client.login(**self.user_data)
        profile_image = {
            'user_profile': self.userProfileInstance.pk,
            'image': self.image_file,
        }

        response_list_data_before_put = self.client.get(self.detail_url).data
        response = self.client.put(self.detail_url, profile_image)
        response_list_data_after_put = self.client.get(self.detail_url).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_list_data_before_put, response_list_data_after_put)

    def test_unauthorized_user_cannot_patch_data(self):
        self.client.logout()
        profile_image = {
            'image': self.image_file,
        }

        response = self.client.patch(self.detail_url, profile_image)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_patch_data(self):
        self.client.login(**self.user_data)
        profile_image = {
            'image': self.image_file,
        }

        response_list_data_before_patch = self.client.get(self.detail_url).data
        response = self.client.patch(self.detail_url, profile_image)
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
