from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel, MajorProjectsInfoModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_MajorProjectsInfoModel
class MajorProjectsInfoModelTest(TestCase):

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

        self.projectInfo = {
            'user_profile': self.userProfileInstance,
            'project_name': fake.word(),
            'company_name': fake.company(),
            'description': fake.text(),
            'start_date': fake.date(),
            'end_date': fake.date_between_dates().strftime('%Y-%m-%d'),
            'currently_working': fake.boolean(),
            'project_url': fake.url(),
            'project_logo': fake.image_url(),
            'featured': fake.boolean(),
        }
        self.projectInfoInstance = MajorProjectsInfoModel.objects.create(**self.projectInfo)

    def test_project_info_str_method(self):
        project_info = MajorProjectsInfoModel.objects.get(id=self.projectInfoInstance.id)
        self.assertEqual(str(project_info), f"{project_info.project_name} - {project_info.start_date}")

    def test_project_info_multiple_instances(self):
        # Create 3 instances of education info
        for inst in range(2,4):
            projectInfo = {
                'user_profile': self.userProfileInstance,
                'project_name': fake.word(),
                'company_name': fake.company(),
                'description': fake.text(),
                'start_date': fake.date(),
                'end_date': fake.date_between_dates().strftime('%Y-%m-%d'),
                'currently_working': fake.boolean(),
                'project_url': fake.url(),
                'project_logo': fake.image_url(),
                'featured': fake.boolean(),
            }
            MajorProjectsInfoModel.objects.create(**projectInfo)

            project_info = MajorProjectsInfoModel.objects.get(id=inst)
            self.assertEqual(str(project_info), f"{project_info.project_name} - {project_info.start_date}")
        self.assertEqual(MajorProjectsInfoModel.objects.filter(user_profile=project_info.user_profile).count(), 3)

    def test_project_info_fields_update(self):
        project_info = MajorProjectsInfoModel.objects.get(id=self.projectInfoInstance.id)
        old_project_info_field_data = self.projectInfo
        new_project_info_field_data = {
            'project_name': fake.word(),
            'company_name': fake.company(),
            'description': fake.text(),
            'start_date': fake.date(),
        }
        project_info.project_name = new_project_info_field_data['project_name']
        project_info.company_name = new_project_info_field_data['company_name']
        project_info.description = new_project_info_field_data['description']
        project_info.start_date = new_project_info_field_data['start_date']

        project_info.save()
        updated_project_info = MajorProjectsInfoModel.objects.get(id=self.projectInfoInstance.id)

        self.assertEqual(str(updated_project_info), f"{new_project_info_field_data['project_name']} - {new_project_info_field_data['start_date']}")
        self.assertNotEqual(str(updated_project_info), f"{old_project_info_field_data['project_name']} - {old_project_info_field_data['start_date']}")

    def test_project_info_only_created_instances_are_accessible(self):
        self.assertTrue(MajorProjectsInfoModel.objects.filter(id=1).exists())
        self.assertFalse(MajorProjectsInfoModel.objects.filter(id=2).exists())
        self.assertFalse(MajorProjectsInfoModel.objects.filter(id=3).exists())

    def test_project_info_deletion_with_direct_delete(self):
        project_info = MajorProjectsInfoModel.objects.get(id=self.projectInfoInstance.id)
        self.assertTrue(MajorProjectsInfoModel.objects.filter(id=self.projectInfoInstance.id).exists())
        project_info.delete()
        self.assertFalse(MajorProjectsInfoModel.objects.filter(id=self.projectInfoInstance.id).exists())

    def test_project_info_deletion_with_user(self):
        self.assertTrue(MajorProjectsInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(MajorProjectsInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
