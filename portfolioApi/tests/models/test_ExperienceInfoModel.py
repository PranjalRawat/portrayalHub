from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel, ExperienceInfoModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_ExperienceInfoModel
class ExperienceInfoModelTest(TestCase):

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
            'phone_number': fake.phone_number(),
        }
        self.userProfileInstance = UserProfileModel.objects.create(**self.user_profile)

        self.experienceInfo = {
            'user_profile': self.userProfileInstance,
            'designation': fake.word(),
            'company_name': fake.company(),
            'start_date': fake.date(),
            'end_date': fake.date_between_dates().strftime('%Y-%m-%d'),
            'currently_working': fake.boolean(),
            'company_logo': fake.image_url(),
            'company_website': fake.url(),
            'featured': fake.boolean(),
            'description': fake.text(),
        }
        ExperienceInfoModel.objects.create(**self.experienceInfo)

    def test_experience_info_str_method(self):
        experience_info = ExperienceInfoModel.objects.get(id=1)
        self.assertEqual(str(experience_info), f"{experience_info.company_name} - {experience_info.designation}")

    def test_experience_info_multiple_instances(self):
        # Create 2 instances of experience info
        experienceInfo = {
            'user_profile': self.userProfileInstance,
            'designation': fake.word(),
            'company_name': fake.company(),
            'start_date': fake.date(),
            'end_date': fake.date_between_dates().strftime('%Y-%m-%d'),
            'currently_working': fake.boolean(),
            'company_logo': fake.image_url(),
            'company_website': fake.url(),
            'featured': fake.boolean(),
            'description': fake.text(),
        }
        ExperienceInfoModel.objects.create(**experienceInfo)

        experience_info = ExperienceInfoModel.objects.get(id=2)
        self.assertEqual(str(experience_info), f"{experience_info.company_name} - {experience_info.designation}")
        self.assertEqual(ExperienceInfoModel.objects.filter(user_profile=experience_info.user_profile).count(), 2)

    def test_experience_info_fields_update(self):
        experience_info = ExperienceInfoModel.objects.get(id=1)
        old_experience_info_field_data = self.experienceInfo
        new_experience_info_field_data = {
            'designation': fake.word(),
            'company_name': fake.company(),
        }
        experience_info.designation = new_experience_info_field_data['designation']
        experience_info.company_name = new_experience_info_field_data['company_name']

        experience_info.save()
        updated_experience_info = ExperienceInfoModel.objects.get(id=1)

        self.assertEqual(str(updated_experience_info), f"{new_experience_info_field_data['company_name']} - {new_experience_info_field_data['designation']}")
        self.assertNotEqual(str(updated_experience_info), f"{old_experience_info_field_data['company_name']} - {old_experience_info_field_data['designation']}")

    def test_experience_info_only_created_instances_are_accessible(self):
        self.assertTrue(ExperienceInfoModel.objects.filter(id=1).exists())
        self.assertFalse(ExperienceInfoModel.objects.filter(id=2).exists())
        self.assertFalse(ExperienceInfoModel.objects.filter(id=3).exists())

    def test_experience_info_deletion_with_direct_delete(self):
        experience_info = ExperienceInfoModel.objects.get(id=1)
        self.assertTrue(ExperienceInfoModel.objects.filter(id=1).exists())
        experience_info.delete()
        self.assertFalse(ExperienceInfoModel.objects.filter(id=1).exists())

    def test_experience_info_deletion_with_user(self):
        self.assertTrue(ExperienceInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(ExperienceInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
