from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from rest_framework import status
from rest_framework.response import Response


# Create your models here.
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
    email = models.EmailField(unique=True)
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
    resume = models.FileField(upload_to = 'resume/', blank = True)
    video_resume = models.FileField(upload_to = 'resume/video_cv/', blank = True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Profile Resume"

class SocialPlatformsModel(models.Model):
    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    platformName = models.CharField(max_length = 255)
    platformIcon = models.ImageField(upload_to = 'social_profiles/')
    profileUrl = models.URLField()
    featured = models.BooleanField(db_index = True, default = True)

    def __str__(self):
        return self.platformName + ' : ' + self.profileUrl

class EducationInfoModel(models.Model):
    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    degree = models.CharField(max_length = 255)
    university = models.CharField(max_length = 255)
    start_date = models.DateField()
    end_date = models.DateField()
    university_logo = models.ImageField(upload_to = 'universities_logo/', blank=True)
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
    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
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

class CertificateInfoModel(models.Model):
    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    course_name = models.CharField(max_length = 255)
    issuing_organization = models.CharField(max_length = 255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null = True, blank = True, default = None)
    credential_url = models.URLField(blank = True)
    course_badge = models.ImageField(upload_to = 'certificates_badge/', blank = True)
    featured = models.BooleanField(db_index = True, default = True)

    def __str__(self):
        return f"{self.course_name} - {self.issuing_organization}"

class SkillsInfoModel(models.Model):
    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    skill = models.CharField(max_length = 100)
    years_of_exp = models.IntegerField(default = 0)
    skill_badge = models.ImageField(upload_to = 'skills_badge/', blank = True)
    featured = models.BooleanField(db_index = True, default = True)

    def __str__(self):
        return f"{self.skill} - {self.years_of_exp}"

class MajorProjectsInfoModel(models.Model):
    user_profile = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    project_name = models.CharField(max_length = 255)
    company_name = models.CharField(max_length = 255, blank = True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null = True, blank = True)
    currently_working = models.BooleanField(db_index = True)
    project_url = models.URLField(blank = True)
    project_logo = models.ImageField(upload_to = 'projects_logo/', blank = True)
    featured = models.BooleanField(db_index = True, default = True)

    def __str__(self):
        return f"{self.project_name} - {self.start_date}"
