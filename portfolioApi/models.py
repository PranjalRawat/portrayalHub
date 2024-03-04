from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SocialPlatformsModel(models.Model):
    platformName = models.CharField(max_length = 255)
    platformIcon = models.ImageField(upload_to='social_profiles/')
    profileUrl = models.URLField()
    featured = models.BooleanField(db_index = True, default = True)

    def __str__(self):
        return self.platformName + ' : ' + self.profileUrl

class UserProfileModel(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ProfileImageModel(models.Model):
    user_profile = models.OneToOneField(UserProfileModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return f"{self.user_profile.user.username}'s Profile Image"
