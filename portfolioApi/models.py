from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response


# Create your models here.

class SocialPlatformsModel(models.Model):
    platformName = models.CharField(max_length = 255)
    platformIcon = models.ImageField(upload_to = 'social_profiles/')
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
    image = models.ImageField(upload_to = 'profile_images/')

    def __str__(self):
        return f"{self.user_profile.user.username}'s Profile Image"

class ResumeUploadModel(models.Model):
    user_profile = models.OneToOneField(UserProfileModel, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/')

    def __str__(self):
        return f"{self.user_profile.user.username}'s Profile Resume"

class EducationInfoModel(models.Model):
    degree = models.CharField(max_length = 255)
    university = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField()
    university_logo = models.ImageField(upload_to = 'university_logo/', blank=True)
    cgpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10.00)
        ],
        blank=True
    )
    featured = models.BooleanField(db_index = True, default = True)

    def __str__(self):
        return f"{self.university} - {self.degree} | {self.cgpa}"

class ExperienceInfoModel(models.Model):
    designation = models.CharField(max_length = 255)
    company_name = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField(null = True, blank = True)
    currently_working = models.BooleanField(db_index = True)
    company_logo = models.ImageField(upload_to = 'company_logo/', blank = True)
    company_website = models.URLField(blank = True)
    featured = models.BooleanField(db_index = True, default = True)
    description = models.TextField()

    def __str__(self):
        return f"{self.company_name} - {self.designation}"
