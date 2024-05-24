from django.conf import settings
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from portfolioApi.models import SkillsInfoModel, UserProfileModel
from portfolioApi.serializers import SkillsInfoSerializer
from faker import Faker
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.views.test_SkillsInfoViewSet
class SkillsInfoViewSetTest(APITestCase):

    def setUpUrl(self):
        self.client.login(**self.user_data)
        self.pk = self.client.get(self.list_url).data[0]['id']
        self.detail_url = reverse('skillsInfo-detail', kwargs={'pk': self.pk})

    def setUp(self):
        self.client = APIClient()
        self.media_fields = ['skill_badge']
        self.list_url = reverse('skillsInfo-list')

        # Create a fake image using PIL
        image = Image.new('RGB', (100, 100))  # You can specify the size of the image as needed

        # Convert the image to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        self.upload_dir = 'skills_badge'
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
            'phone_number': '123456789',
        }
        self.userProfileInstance = UserProfileModel.objects.create(**self.user_profile)

        for ins in range(5):
            SkillsInfoModel.objects.create(**{
                'user_profile': self.userProfileInstance,
                'skill': fake.word(),
                'years_of_exp': fake.random_int(min=0, max=5),
                'proficiency': fake.random_int(min=0, max=10),
                'skill_badge': fake.image_url(),
                'featured': fake.boolean(),
            })
        self.setUpUrl()

    def tearDown(self):
        super().tearDown()
        # Delete the created image file from the media directory
        image_file_path = os.path.join(settings.MEDIA_ROOT, self.upload_dir, self.image_name)
        if os.path.exists(image_file_path):
            os.remove(image_file_path)

    def test_user_skills_info_list_view(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(SkillsInfoSerializer(SkillsInfoModel.objects.filter(user_profile=self.userProfileInstance), many=True).data), len(response.data))

        serialized_data = SkillsInfoSerializer(SkillsInfoModel.objects.filter(user_profile=self.userProfileInstance), many=True).data
        view_data = response.data

        list_view_count = len(response.data)
        for view_count in range(list_view_count):
            view_data_item = view_data[view_count]
            serialized_data_item = serialized_data[view_count]
            for key in view_data_item:
                if key in self.media_fields:
                    self.assertIn(serialized_data_item[key], view_data_item[key])
                else:
                    self.assertEqual(serialized_data_item[key], view_data_item[key])

    def test_user_skills_info_detail_view(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data_item = SkillsInfoSerializer(SkillsInfoModel.objects.get(id=self.pk)).data
        view_data_item = response.data

        for key in view_data_item:
            if key in self.media_fields:
                self.assertIn(serialized_data_item[key], view_data_item[key])
            else:
                self.assertEqual(serialized_data_item[key], view_data_item[key])

    def test_unauthorized_user_cannot_post_data(self):
        self.client.logout()
        skillsInfo = {
            'user_profile': self.userProfileInstance.pk,
            'skill': fake.word(),
            'years_of_exp': fake.random_int(min=0, max=5),
            'proficiency': fake.random_int(min=0, max=10),
            'skill_badge': self.image_file,
            'featured': fake.boolean(),
        }
        response = self.client.post(self.list_url, skillsInfo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_post_data(self):
        self.client.login(**self.user_data)
        skillsInfo = {
            'user_profile': self.userProfileInstance.pk,
            'skill': fake.word(),
            'years_of_exp': fake.random_int(min=0, max=5),
            'proficiency': fake.random_int(min=0, max=10),
            'skill_badge': self.image_file,
            'featured': fake.boolean(),
        }
        response_list_data_before_post = self.client.get(self.list_url).data
        response = self.client.post(self.list_url, skillsInfo)
        response_list_data_after_post = self.client.get(self.list_url).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_list_data_before_post), len(response_list_data_after_post) - 1)

    def test_unauthorized_user_cannot_put_data(self):
        self.client.logout()
        skillsInfo = {
            'user_profile': self.userProfileInstance.pk,
            'skill': fake.word(),
            'years_of_exp': fake.random_int(min=0, max=5),
            'proficiency': fake.random_int(min=0, max=10),
            'skill_badge': self.image_file,
            'featured': fake.boolean(),
        }

        response = self.client.put(self.detail_url, skillsInfo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_put_data(self):
        self.client.login(**self.user_data)
        skillsInfo = {
            'user_profile': self.userProfileInstance.pk,
            'skill': fake.word(),
            'years_of_exp': fake.random_int(min=0, max=5),
            'proficiency': fake.random_int(min=0, max=10),
            'skill_badge': self.image_file,
            'featured': fake.boolean(),
        }

        response_list_data_before_put = self.client.get(self.detail_url).data
        response = self.client.put(self.detail_url, skillsInfo)
        response_list_data_after_put = self.client.get(self.detail_url).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_list_data_before_put, response_list_data_after_put)

    def test_unauthorized_user_cannot_patch_data(self):
        self.client.logout()
        skillsInfo = {
            'user_profile': self.userProfileInstance.pk,
            'skill': fake.word(),
            'featured': fake.boolean(),
        }

        response = self.client.patch(self.detail_url, skillsInfo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_patch_data(self):
        self.client.login(**self.user_data)
        skillsInfo = {
            'user_profile': self.userProfileInstance.pk,
            'skill': fake.word(),
            'featured': fake.boolean(),
        }

        response_list_data_before_patch = self.client.get(self.detail_url).data
        response = self.client.patch(self.detail_url, skillsInfo)
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
