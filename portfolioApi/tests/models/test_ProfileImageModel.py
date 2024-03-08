from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import ProfileImageModel, UserProfileModel
from faker import Faker

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_ProfileImageModel
class ProfileImageModelTest(TestCase):

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

        self.profile_image = {
            'user_profile': self.userProfileInstance,
            'image': fake.image_url(),
        }
        ProfileImageModel.objects.create(**self.profile_image)

    def test_profile_image_str_method(self):
        user_profile_image = ProfileImageModel.objects.get(id=1)
        self.assertEqual(str(user_profile_image), f"{user_profile_image.user_profile.user.username}'s Profile Image")

    def test_user_single_profile_image_instance(self):
        with self.assertRaises(Exception) as context:
            # Attempt to create another user image instance for the same user profile
            ProfileImageModel.objects.create(
                user_profile = self.userProfileInstance,
                image = fake.image_url(),
            )
            self.assertTrue('unique constraint' in str(context.exception))

    def test_user_profile_image_deletion_with_user(self):
        user_profile_image = ProfileImageModel.objects.get(id=1)
        self.assertTrue(ProfileImageModel.objects.filter(user_profile=user_profile_image.user_profile).exists())
        user_profile_image.user_profile.user.delete()
        self.assertFalse(ProfileImageModel.objects.filter(user_profile=user_profile_image.user_profile).exists())

    def test_user_profile_image_deletion_with_direct_delete(self):
        user_profile_image = ProfileImageModel.objects.get(id=1)
        self.assertTrue(ProfileImageModel.objects.filter(user_profile=user_profile_image.user_profile).exists())
        user_profile_image.delete()
        self.assertFalse(ProfileImageModel.objects.filter(user_profile=user_profile_image.user_profile).exists())

    def test_user_profile_image_update(self):
        user_profile_image = ProfileImageModel.objects.get(id=1)
        old_image = user_profile_image.image
        new_image = fake.image_url()
        user_profile_image.image = new_image
        user_profile_image.save()
        updated_user_profile_image = ProfileImageModel.objects.get(id=1)
        self.assertEqual(updated_user_profile_image.image, new_image)
        self.assertNotEqual(updated_user_profile_image.image, old_image)
