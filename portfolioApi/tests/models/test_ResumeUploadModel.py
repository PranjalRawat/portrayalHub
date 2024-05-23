from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel, ResumeUploadModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_ResumeUploadModel
class ResumeUploadModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user_data = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': fake.password(),
        }
        self.userInstance = User.objects.create(**self.user_data)

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

        self.user_resume_data = {
            'user_profile': self.userProfileInstance,
            'resume': fake.file_path(extension='pdf', category='document', depth=1),
            'video_resume': fake.file_path(extension='mp4', category='video', depth=1),
            'cover_letter': fake.word(),
            'designation': fake.company(),
        }

        self.userResumeInstance = ResumeUploadModel.objects.create(**self.user_resume_data)

    def test_user_resume_str_method(self):
        user_profile_resume = ResumeUploadModel.objects.get(id=self.userResumeInstance.id)
        self.assertEqual(str(user_profile_resume), f"{self.userProfileInstance.user.username}'s Profile Resume")

    def test_user_single_profile_resume_instance(self):
        with self.assertRaises(Exception) as context:
            # Attempt to create another user resume instance for the same user profile
            ResumeUploadModel.objects.create(
                user_profile = self.userProfileInstance,
                resume = fake.file_path(extension='pdf', category='document', depth=1),
                video_resume = fake.file_path(extension='mp4', category='video', depth=1),
                cover_letter = fake.word(),
                designation = fake.company(),
            )
            self.assertTrue('unique constraint' in str(context.exception))

    def test_user_profile_resume_deletion_with_user(self):
        self.assertTrue(ResumeUploadModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(ResumeUploadModel.objects.filter(user_profile=self.userProfileInstance).exists())

    def test_user_profile_resume_deletion_with_direct_delete(self):
        user_profile_resume = ResumeUploadModel.objects.get(id=self.userResumeInstance.id)
        self.assertTrue(ResumeUploadModel.objects.filter(user_profile=self.userProfileInstance).exists())
        user_profile_resume.delete()
        self.assertFalse(ResumeUploadModel.objects.filter(user_profile=self.userProfileInstance).exists())

    def test_user_profile_resume_document_resume_validity(self):
        user_profile_resume = ResumeUploadModel.objects.get(id=self.userResumeInstance.id)
        self.assertTrue(user_profile_resume.resume == self.user_resume_data['resume'])
        self.assertTrue(user_profile_resume.resume.url.endswith('.pdf'))

    def test_user_profile_resume_video_resume_validity(self):
        user_profile_resume = ResumeUploadModel.objects.get(id=self.userResumeInstance.id)
        self.assertTrue(user_profile_resume.video_resume == self.user_resume_data['video_resume'])
        self.assertTrue(user_profile_resume.video_resume.url.endswith('.mp4'))
