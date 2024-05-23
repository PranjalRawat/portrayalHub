from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel, SkillsInfoModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_SkillsInfoModel
class SkillsInfoModelTest(TestCase):

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

        self.skillsInfo = {
            'user_profile': self.userProfileInstance,
            'skill': fake.word(),
            'years_of_exp': fake.random_int(min=0, max=5),
            'proficiency': fake.random_int(min=0, max=10),
            'skill_badge': fake.image_url(),
            'featured': fake.boolean(),
        }
        self.skillsInfoInstance = SkillsInfoModel.objects.create(**self.skillsInfo)

    def test_skills_info_str_method(self):
        skills_info = SkillsInfoModel.objects.get(id=self.skillsInfoInstance.id)
        self.assertEqual(str(skills_info), f"{skills_info.skill} - {skills_info.years_of_exp}")

    def test_skills_info_multiple_instances(self):
        # Create 10 instances of education info
        for inst in range(2,11):
            skillsInfo = {
                'user_profile': self.userProfileInstance,
                'skill': fake.word(),
                'years_of_exp': fake.random_int(min=0, max=5),
                'proficiency': fake.random_int(min=0, max=10),
                'skill_badge': fake.image_url(),
                'featured': fake.boolean(),
            }
            SkillsInfoModel.objects.create(**skillsInfo)

            skills_info = SkillsInfoModel.objects.get(id=inst)
            self.assertEqual(str(skills_info), f"{skills_info.skill} - {skills_info.years_of_exp}")
        self.assertEqual(SkillsInfoModel.objects.filter(user_profile=skills_info.user_profile).count(), 10)

    def test_skills_info_fields_update(self):
        skills_info = SkillsInfoModel.objects.get(id=self.skillsInfoInstance.id)
        old_skills_info_field_data = self.skillsInfo
        new_skills_info_field_data = {
            'skill': fake.word(),
            'years_of_exp': fake.random_int(min=0, max=5),
            'proficiency': fake.random_int(min=0, max=10),
            'skill_badge': fake.image_url(),
            'featured': fake.boolean(),
        }
        skills_info.skill = new_skills_info_field_data['skill']
        skills_info.years_of_exp = new_skills_info_field_data['years_of_exp']
        skills_info.skill_badge = new_skills_info_field_data['skill_badge']
        skills_info.featured = new_skills_info_field_data['featured']

        skills_info.save()
        updated_skills_info = SkillsInfoModel.objects.get(id=self.skillsInfoInstance.id)

        self.assertEqual(str(updated_skills_info), f"{new_skills_info_field_data['skill']} - {new_skills_info_field_data['years_of_exp']}")
        self.assertNotEqual(str(updated_skills_info), f"{old_skills_info_field_data['skill']} - {old_skills_info_field_data['years_of_exp']}")

    def test_skills_info_only_created_instances_are_accessible(self):
        self.assertTrue(SkillsInfoModel.objects.filter(id=1).exists())
        self.assertFalse(SkillsInfoModel.objects.filter(id=2).exists())
        self.assertFalse(SkillsInfoModel.objects.filter(id=3).exists())

    def test_skills_info_deletion_with_direct_delete(self):
        skills_info = SkillsInfoModel.objects.get(id=self.skillsInfoInstance.id)
        self.assertTrue(SkillsInfoModel.objects.filter(id=self.skillsInfoInstance.id).exists())
        skills_info.delete()
        self.assertFalse(SkillsInfoModel.objects.filter(id=self.skillsInfoInstance.id).exists())

    def test_skills_info_deletion_with_user(self):
        self.assertTrue(SkillsInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(SkillsInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
