from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel, CertificateInfoModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_CertificateInfoModel
class CertificateInfoModelTest(TestCase):

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

        self.certificateInfo = {
            'user_profile': self.userProfileInstance,
            'course_name': fake.word(),
            'issuing_organization': fake.company(),
            'issue_date': fake.date(),
            'expiration_date': fake.random_element(elements = (None, fake.date_between_dates().strftime('%Y-%m-%d')) ),
            'credential_url': fake.url(),
            'course_badge': fake.image_url(),
            'featured': fake.boolean(),
        }
        CertificateInfoModel.objects.create(**self.certificateInfo)

    def test_certificate_info_str_method(self):
        certificate_info = CertificateInfoModel.objects.get(id=1)
        self.assertEqual(str(certificate_info), f"{certificate_info.course_name} - {certificate_info.issuing_organization}")

    def test_certificate_info_multiple_instances(self):
        # Create 3 instances of education info
        for inst in range(2,4):
            certificateInfo = {
                'user_profile': self.userProfileInstance,
                'course_name': fake.word(),
                'issuing_organization': fake.company(),
                'issue_date': fake.date(),
                'expiration_date': fake.random_element(elements = (None, fake.date_between_dates().strftime('%Y-%m-%d')) ),
                'credential_url': fake.url(),
                'course_badge': fake.image_url(),
                'featured': fake.boolean(),
            }
            CertificateInfoModel.objects.create(**certificateInfo)

            certificate_info = CertificateInfoModel.objects.get(id=inst)
            self.assertEqual(str(certificate_info), f"{certificate_info.course_name} - {certificate_info.issuing_organization}")
        self.assertEqual(CertificateInfoModel.objects.filter(user_profile=certificate_info.user_profile).count(), 3)

    def test_certificate_info_fields_update(self):
        certificate_info = CertificateInfoModel.objects.get(id=1)
        old_certificate_info_field_data = self.certificateInfo
        new_certificate_info_field_data = {
            'course_name': fake.word(),
            'issuing_organization': fake.company(),
            'credential_url': fake.url(),
            'course_badge': fake.image_url(),
        }
        certificate_info.course_name = new_certificate_info_field_data['course_name']
        certificate_info.issuing_organization = new_certificate_info_field_data['issuing_organization']
        certificate_info.credential_url = new_certificate_info_field_data['credential_url']
        certificate_info.course_badge = new_certificate_info_field_data['course_badge']

        certificate_info.save()
        updated_certificate_info = CertificateInfoModel.objects.get(id=1)

        self.assertEqual(str(updated_certificate_info), f"{new_certificate_info_field_data['course_name']} - {new_certificate_info_field_data['issuing_organization']}")
        self.assertNotEqual(str(updated_certificate_info), f"{old_certificate_info_field_data['course_name']} - {old_certificate_info_field_data['issuing_organization']}")

    def test_certificate_info_only_created_instances_are_accessible(self):
        self.assertTrue(CertificateInfoModel.objects.filter(id=1).exists())
        self.assertFalse(CertificateInfoModel.objects.filter(id=2).exists())
        self.assertFalse(CertificateInfoModel.objects.filter(id=3).exists())

    def test_certificate_info_deletion_with_direct_delete(self):
        certificate_info = CertificateInfoModel.objects.get(id=1)
        self.assertTrue(CertificateInfoModel.objects.filter(id=1).exists())
        certificate_info.delete()
        self.assertFalse(CertificateInfoModel.objects.filter(id=1).exists())

    def test_certificate_info_deletion_with_user(self):
        self.assertTrue(CertificateInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(CertificateInfoModel.objects.filter(user_profile=self.userProfileInstance).exists())
