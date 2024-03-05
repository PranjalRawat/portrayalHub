from rest_framework import serializers
from .models import SocialPlatformsModel, UserProfileModel, ProfileImageModel, ResumeUploadModel, EducationInfoModel

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
