from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import SocialPlatformsModel, UserProfileModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_SocialPlatformsModel
class SocialPlatformModelTest(TestCase):

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

        self.socialPlatform = {
            'user_profile': self.userProfileInstance,
            'platformName': fake.company(),
            'platformIcon': fake.image_url(),
            'profileUrl': fake.url(),
            'featured': fake.boolean()
        }

        SocialPlatformsModel.objects.create(**self.socialPlatform)

    def test_social_platform_str_method(self):
        social_platform = SocialPlatformsModel.objects.get(id=1)
        self.assertEqual(str(social_platform), f"{social_platform.platformName} : {social_platform.profileUrl}")

    def test_social_platform_multiple_instances(self):
        # Create 5 instances of social platforms
        for inst in range(2,6):
            socialPlatformNew = {
                'user_profile': self.userProfileInstance,
                'platformName': fake.company(),
                'platformIcon': fake.image_url(),
                'profileUrl': fake.url(),
                'featured': fake.boolean()
            }

            SocialPlatformsModel.objects.create(**socialPlatformNew)

            social_platform = SocialPlatformsModel.objects.get(id=inst)
            self.assertEqual(str(social_platform), f"{social_platform.platformName} : {social_platform.profileUrl}")
        self.assertEqual(SocialPlatformsModel.objects.filter(user_profile=social_platform.user_profile).count(), 5)

    def test_social_platform_fields_update(self):
        social_platform = SocialPlatformsModel.objects.get(id=1)
        old_social_platform_field_data = self.socialPlatform
        new_social_platform_field_data = {
            'platformName': fake.company(),
            'platformIcon': fake.image_url(),
            'profileUrl': fake.url(),
            'featured': fake.boolean()
        }
        social_platform.platformName = new_social_platform_field_data['platformName']
        social_platform.platformIcon = new_social_platform_field_data['platformIcon']
        social_platform.profileUrl = new_social_platform_field_data['profileUrl']
        social_platform.featured = new_social_platform_field_data['featured']

        social_platform.save()
        updated_social_platform = SocialPlatformsModel.objects.get(id=1)

        self.assertEqual(str(updated_social_platform), f"{new_social_platform_field_data['platformName']} : {new_social_platform_field_data['profileUrl']}")
        self.assertNotEqual(str(updated_social_platform), f"{old_social_platform_field_data['platformName']} : {old_social_platform_field_data['profileUrl']}")

    def test_social_platform_only_created_instances_are_accessible(self):
        self.assertTrue(SocialPlatformsModel.objects.filter(id=1).exists())
        self.assertFalse(SocialPlatformsModel.objects.filter(id=2).exists())
        self.assertFalse(SocialPlatformsModel.objects.filter(id=3).exists())

    def test_social_platform_deletion_with_direct_delete(self):
        social_platform = SocialPlatformsModel.objects.get(id=1)
        self.assertTrue(SocialPlatformsModel.objects.filter(id=1).exists())
        social_platform.delete()
        self.assertFalse(SocialPlatformsModel.objects.filter(id=1).exists())

    def test_social_platform_deletion_with_user(self):
        self.assertTrue(SocialPlatformsModel.objects.filter(user_profile=self.userProfileInstance).exists())
        self.userProfileInstance.user.delete()
        self.assertFalse(SocialPlatformsModel.objects.filter(user_profile=self.userProfileInstance).exists())
