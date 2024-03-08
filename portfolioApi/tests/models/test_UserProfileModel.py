from django.test import TestCase
from django.contrib.auth.models import User
from portfolioApi.models import UserProfileModel
from faker import Faker
from datetime import date

fake = Faker()

# Test Execution Command :::>>>  python3 manage.py test portfolioApi.tests.models.test_UserProfileModel
class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user_data = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': fake.password(),
        }
        self.user = User.objects.create(**self.user_data)

        self.profile_data = {
            'user' : self.user,
            'first_name' : fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(),
            'gender': fake.random_element(elements = ('M', 'F', 'O')),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
        }
        UserProfileModel.objects.create(**self.profile_data)

    def test_user_profile_str_method(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertEqual(str(user_profile), f"{user_profile.user.username}'s Profile")

    def test_user_profile_has_user(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertIsInstance(user_profile.user, User)

    def test_user_profile_first_name_validity(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertTrue(user_profile.first_name == self.profile_data['first_name'])

    def test_user_profile_last_name_validity(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertTrue(user_profile.last_name == self.profile_data['last_name'])

    def test_user_profile_date_of_birth_validity(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertTrue(user_profile.date_of_birth == self.profile_data['date_of_birth'])
        self.assertTrue(user_profile.date_of_birth <= date.today())

    def test_user_profile_email_format(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertTrue('@' in user_profile.email)

    def test_user_profile_email_unique(self):
        # Try creating another user profile with the same email, should raise IntegrityError
        with self.assertRaises(Exception) as context:
            UserProfileModel.objects.create(
                user = User.objects.create(username=fake.user_name(), email=fake.email(), password=fake.password()),
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                date_of_birth = fake.date_of_birth(),
                gender = fake.random_element(elements=('M', 'F', 'O')),
                address = fake.address(),
                email = self.profile_data['email'],  # Use the same email as the first user profile
                phone_number = fake.phone_number(),
            )
            self.assertTrue('unique constraint' in str(context.exception))

    def test_user_profile_address_not_empty(self):
        user_profile = UserProfileModel.objects.get(id=1)
        self.assertTrue(user_profile.address != '')

    def test_user_profile_gender_choices(self):
        user_profile = UserProfileModel.objects.get(id=1)
        valid_genders = [choice[0] for choice in UserProfileModel.GENDER_CHOICES]
        self.assertIn(user_profile.gender, valid_genders)

    def test_user_profile_update(self):
        user_profile = UserProfileModel.objects.get(id=1)
        old_first_name = user_profile.first_name
        new_first_name = fake.first_name()
        user_profile.first_name = new_first_name
        user_profile.save()
        updated_user_profile = UserProfileModel.objects.get(id=1)
        self.assertEqual(updated_user_profile.first_name, new_first_name)
        self.assertNotEqual(updated_user_profile.first_name, old_first_name)

    def test_user_profile_deletion_cascade(self):
        user_profile = UserProfileModel.objects.get(id=1)
        user = user_profile.user
        user.delete()
        with self.assertRaises(UserProfileModel.DoesNotExist):
            UserProfileModel.objects.get(user=user)

    def test_user_single_user_profile_instance(self):
        with self.assertRaises(Exception) as context:
            # Attempt to create another user profile for the same user
            UserProfileModel.objects.create(
                user = self.user,
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                date_of_birth = fake.date_of_birth(),
                gender = fake.random_element(elements=('M', 'F', 'O')),
                address = fake.address(),
                email = fake.email(),
                phone_number = fake.phone_number(),
            )
            self.assertTrue('unique constraint' in str(context.exception))
