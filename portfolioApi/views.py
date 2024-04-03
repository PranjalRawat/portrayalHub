from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import SocialPlatformsModel, UserProfileModel, ProfileImageModel, ResumeUploadModel, EducationInfoModel, ExperienceInfoModel, CertificateInfoModel, SkillsInfoModel, MajorProjectsInfoModel
from .serializers import SocialPlatformSerializer, UserProfileSerializer, UserProfileImageSerializer, ResumeUploadSerializer, EducationInfoSerializer, ExperienceInfoSerializer, CertificateInfoSerializer, SkillsInfoSerializer, MajorProjectsInfoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status

class SocialPlatformViewSet(viewsets.ModelViewSet):
    serializer_class = SocialPlatformSerializer
    search_fields = ['platformName']
    ordering_fields = ['id']

    def get_queryset(self):
        return SocialPlatformsModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfileModel.objects.filter(user=self.request.user)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Check if a UserProfile instance already exists for the user
        user_profile_exists = self.get_queryset().exists()

        # If a UserProfile instance already exists, disallow the creation (POST) action
        if user_profile_exists:
            return Response({'detail': 'You already have a profile. Updating existing profile is allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Otherwise, proceed with the normal creation (POST) action
        return super().create(request, *args, **kwargs)

class UserProfileImageViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileImageSerializer

    def get_queryset(self):
        return ProfileImageModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Check if a UserProfile instance already exists for the user
        user_profile_pic_exists = self.get_queryset().exists()

        # If a UserProfile instance already exists, disallow the creation (POST) action
        if user_profile_pic_exists:
            return Response({'detail': 'You already have a profile picture. Updating existing profile picture is allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Otherwise, proceed with the normal creation (POST) action
        return super().create(request, *args, **kwargs)

class ResumeUploadViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeUploadSerializer

    def get_queryset(self):
        return ResumeUploadModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Check if a UserProfile instance already exists for the user
        user_profile_pic_exists = self.get_queryset().exists()

        # If a UserProfile instance already exists, disallow the creation (POST) action
        if user_profile_pic_exists:
            return Response({'detail': 'You already have a profile resume. Updating existing profile resume is allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Otherwise, proceed with the normal creation (POST) action
        return super().create(request, *args, **kwargs)

class EducationInfoViewSet(viewsets.ModelViewSet):
    serializer_class = EducationInfoSerializer
    search_fields = ['degree', 'university']
    ordering_fields = ['cgpa', 'end_date']

    def get_queryset(self):
        return EducationInfoModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class ExperienceInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceInfoSerializer
    search_fields = ['company_name', 'designation']
    ordering_fields = ['end_date']

    def get_queryset(self):
        return ExperienceInfoModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        currently_working = self.request.data.get('currently_working', False)

        if currently_working and ExperienceInfoModel.objects.filter(currently_working=True).exists():
            return Response({'detail': 'Only one instance can have currently_working as True.'}, status=400)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        currently_working = self.request.data.get('currently_working', False)

        if currently_working and ExperienceInfoModel.objects.filter(currently_working=True).exclude(pk=instance.pk).exists():
            return Response({'detail': 'Only one instance can have currently_working as True.'}, status=400)

        if currently_working:
            instance.end_date = None
            instance.save()

        return super().update(request, *args, **kwargs)

class CertificateInfoViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateInfoSerializer

    def get_queryset(self):
        return CertificateInfoModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class SkillsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = SkillsInfoSerializer

    def get_queryset(self):
        return SkillsInfoModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class MajorProjectsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = MajorProjectsInfoSerializer
    search_fields = ['project_name']

    def get_queryset(self):
        return MajorProjectsInfoModel.objects.filter(user_profile=self.request.user.pk)

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

