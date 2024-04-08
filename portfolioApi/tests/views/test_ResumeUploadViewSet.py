from django.conf import settings
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from portfolioApi.models import ResumeUploadModel, UserProfileModel
from portfolioApi.serializers import ResumeUploadSerializer
from faker import Faker
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.views.test_ResumeUploadViewSet
class ResumeUploadViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.media_fields = ['resume', 'video_resume']
        self.list_url = reverse('userprofileResume-list')
        self.pk = 1
        self.detail_url = reverse('userprofileResume-detail', kwargs={'pk': self.pk})

        # Create a fake image using PIL
        pdf = Image.new('RGB', (100, 100))  # You can specify the size of the image as needed

        # Convert the image to bytes
        pdf_bytes = BytesIO()
        pdf.save(pdf_bytes, format='PDF')
        self.upload_dir = 'resume'
        self.pdf_name = 'pdf_image.pdf'
        # Create a SimpleUploadedFile object from the pdf bytes
        self.pdf_file = SimpleUploadedFile(self.pdf_name, pdf_bytes.getvalue(), content_type='text/pdf')

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

        self.user_resume_data = {
            'user_profile': self.userProfileInstance,
            'resume': fake.file_path(extension='pdf', category='document', depth=1),
            'video_resume': fake.file_path(extension='mp4', category='video', depth=1),
            'cover_letter': fake.word(),
            'designation': fake.company(),
        }
        ResumeUploadModel.objects.create(**self.user_resume_data)

    def tearDown(self):
        super().tearDown()
        # Delete the created image file from the media directory
        image_file_path = os.path.join(settings.MEDIA_ROOT, self.upload_dir, self.pdf_name)
        if os.path.exists(image_file_path):
            os.remove(image_file_path)

    def test_user_profile_resume_list_view(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = ResumeUploadSerializer(ResumeUploadModel.objects.filter(user_profile=self.userProfileInstance), many=True).data[0]
        view_data = response.data[0]

        self.assertEqual(len(serialized_data), len(view_data))
        for key in view_data:
            if key in self.media_fields:
                self.assertIn(serialized_data[key], view_data[key])
            else:
                self.assertEqual(serialized_data[key], view_data[key])

    def test_user_profile_resume_detail_view(self):
        self.client.login(**self.user_data)
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = ResumeUploadSerializer(ResumeUploadModel.objects.get(id=self.pk)).data
        view_data = response.data

        for key in view_data:
            if key in self.media_fields:
                self.assertIn(serialized_data[key], view_data[key])
            else:
                self.assertEqual(serialized_data[key], view_data[key])

    def test_user_profile_resume_can_have_only_one_instance(self):
        self.client.login(**self.user_data)
        user_resume_data = {
            'user_profile': self.userProfileInstance.pk,
            'resume': self.pdf_file,
            'video_resume': self.pdf_file,
            'cover_letter': fake.word(),
            'designation': fake.company(),
        }
        response = self.client.post(self.list_url, user_resume_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_user_cannot_put_data(self):
        self.client.logout()
        user_resume_data = {
            'user_profile': self.userProfileInstance.pk,
            'resume':  self.pdf_file,
        }

        response = self.client.put(self.detail_url, user_resume_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_put_data(self):
        self.client.login(**self.user_data)
        user_resume_data = {
            'user_profile': self.userProfileInstance.pk,
            'resume': self.pdf_file,
            'cover_letter': fake.word(),
            'designation': fake.company(),
        }

        response_list_data_before_put = self.client.get(self.detail_url).data
        response = self.client.put(self.detail_url, user_resume_data)
        response_list_data_after_put = self.client.get(self.detail_url).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response_list_data_before_put, response_list_data_after_put)

    def test_unauthorized_user_cannot_patch_data(self):
        self.client.logout()
        user_resume_data = {
            'user_profile': self.userProfileInstance.pk,
            'resume': self.pdf_file,
        }

        response = self.client.patch(self.detail_url, user_resume_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_can_patch_data(self):
        self.client.login(**self.user_data)
        user_resume_data = {
            'user_profile': self.userProfileInstance.pk,
            'resume': self.pdf_file,
        }

        response_list_data_before_patch = self.client.get(self.detail_url).data
        response = self.client.patch(self.detail_url, user_resume_data)
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
