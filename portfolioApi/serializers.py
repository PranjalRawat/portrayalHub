from rest_framework import serializers
from .models import SocialPlatformsModel, UserProfileModel, ProfileImageModel, ResumeUploadModel, EducationInfoModel, ExperienceInfoModel, CertificateInfoModel, SkillsInfoModel, MajorProjectsInfoModel

class SocialPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPlatformsModel
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = '__all__'

class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImageModel
        fields = '__all__'

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeUploadModel
        fields = '__all__'

class EducationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationInfoModel
        fields = '__all__'

class ExperienceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceInfoModel
        fields = '__all__'

class CertificateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateInfoModel
        fields = '__all__'

class SkillsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillsInfoModel
        fields = '__all__'

class MajorProjectsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorProjectsInfoModel
        fields = '__all__'
