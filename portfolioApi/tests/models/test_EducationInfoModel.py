from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import EducationInfoModel, UserProfileModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_EducationInfoModel
class EducationInfoModelTest(TestCase):

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

        self.educationInfo = {
            'user_profile': self.userProfileInstance,
            'degree': fake.word(),
            'university': fake.company(),
            'start_date': fake.date(),
            'end_date': fake.date_between_dates().strftime('%Y-%m-%d'),
            'university_logo': fake.image_url(),
            'cgpa': float(fake.pydecimal(left_digits=1, right_digits=1, positive=False, min_value=0, max_value=9)),
            'featured': fake.boolean()
        }
        self.educationInfoInstance = EducationInfoModel.objects.create(**self.educationInfo)

    def test_education_info_str_method(self):
        education_info = EducationInfoModel.objects.get(id=self.educationInfoInstance.id)
        self.assertEqual(str(education_info), f"{education_info.university} - {education_info.degree} | {education_info.cgpa}")

    def test_education_info_multiple_instances(self):
        # Create 5 instances of education info
        for inst in range(2,6):
            educationInfo = {
                'user_profile': self.userProfileInstance,
                'degree': fake.word(),
                'university': fake.company(),
                'start_date': fake.date(),
                'end_date': fake.date_between_dates().strftime('%Y-%m-%d'),
                'university_logo': fake.image_url(),
                'cgpa': float(fake.pydecimal(left_digits=1, right_digits=2, positive=False, min_value=0, max_value=9.99)),
                'featured': fake.boolean()
            }
            EducationInfoModel.objects.create(**educationInfo)

            education_info = EducationInfoModel.objects.get(id=inst)
            self.assertEqual(str(education_info), f"{education_info.university} - {education_info.degree} | {education_info.cgpa}")
        self.assertEqual(EducationInfoModel.objects.filter(user_profile=education_info.user_profile).count(), 5)

    def test_education_info_fields_update(self):
        education_info = EducationInfoModel.objects.get(id=self.educationInfoInstance.id)
        old_education_info_field_data = self.educationInfo
        new_education_info_field_data = {
            'degree': fake.word(),
            'university': fake.company(),
            'university_logo': fake.image_url(),
            'cgpa': float(fake.pydecimal(left_digits=1, right_digits=2, positive=False, min_value=0, max_value=9.99)),
        }
        education_info.degree = new_education_info_field_data['degree']
        education_info.university = new_education_info_field_data['university']
        education_info.university_logo = new_education_info_field_data['university_logo']
        education_info.cgpa = new_education_info_field_data['cgpa']

        education_info.save()
        updated_education_info = EducationInfoModel.objects.get(id=self.educationInfoInstance.id)

        self.assertEqual(str(updated_education_info), f"{new_education_info_field_data['university']} - {new_education_info_field_data['degree']} | {new_education_info_field_data['cgpa']}")
        self.assertNotEqual(str(updated_education_info), f"{old_education_info_field_data['university']} - {old_education_info_field_data['degree']} | {old_education_info_field_data['cgpa']}")

    def test_education_info_only_created_instances_are_accessible(self):
        self.assertTrue(EducationInfoModel.objects.filter(id=1).exists())
        self.assertFalse(EducationInfoModel.objects.filter(id=2).exists())
        self.assertFalse(EducationInfoModel.objects.filter(id=3).exists())

    def test_education_info_deletion_with_direct_delete(self):
        education_info = EducationInfoModel.objects.get(id=self.educationInfoInstance.id)
        self.assertTrue(EducationInfoModel.objects.filter(id=self.educationInfoInstance.id).exists())
        education_info.delete()
        self.assertFalse(EducationInfoModel.objects.filter(id=self.educationInfoInstance.id).exists())

    def test_education_info_deletion_with_user(self):
        self.assertTrue(EducationInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(EducationInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
