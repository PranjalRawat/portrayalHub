from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView

from .models import SocialPlatformsModel, UserProfileModel, ProfileImageModel, ResumeUploadModel, EducationInfoModel, ExperienceInfoModel, CertificateInfoModel, SkillsInfoModel, MajorProjectsInfoModel
from .serializers import SocialPlatformSerializer, UserProfileSerializer, UserProfileImageSerializer, ResumeUploadSerializer, EducationInfoSerializer, ExperienceInfoSerializer, CertificateInfoSerializer, SkillsInfoSerializer, MajorProjectsInfoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status

class SocialPlatformViewSet(viewsets.ModelViewSet):
    serializer_class = SocialPlatformSerializer
    search_fields = ['platformName']
    ordering_fields = ['id']

    def get_queryset(self):
        return SocialPlatformsModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class OtherSocialPlatformView(APIView):
    serializer_class = SocialPlatformSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = SocialPlatformsModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"social_platforms": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfileModel.objects.filter(user=self.request.user)

    def get_permissions(self):
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

class OtherUserProfileView(APIView):
    serializer_class = UserProfileSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                serializer = self.serializer_class(user_profile)
                return Response({"user_info": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserProfileImageViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileImageSerializer

    def get_queryset(self):
        return ProfileImageModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
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

class OtherUserProfileImageView(APIView):
    serializer_class = UserProfileImageSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = ProfileImageModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"user_image": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ResumeUploadViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeUploadSerializer

    def get_queryset(self):
        return ResumeUploadModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
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

class OtherResumeUploadView(APIView):
    serializer_class = ResumeUploadSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = ResumeUploadModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"user_resume": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class EducationInfoViewSet(viewsets.ModelViewSet):
    serializer_class = EducationInfoSerializer
    search_fields = ['degree', 'university']
    ordering_fields = ['cgpa', 'end_date']

    def get_queryset(self):
        return EducationInfoModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class OtherEducationInfoView(APIView):
    serializer_class = EducationInfoSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = EducationInfoModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"education_info": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ExperienceInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceInfoSerializer
    search_fields = ['company_name', 'designation']
    ordering_fields = ['end_date']

    def get_queryset(self):
        return ExperienceInfoModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
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

class OtherExperienceInfoView(APIView):
    serializer_class = ExperienceInfoSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = ExperienceInfoModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"experience_info": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class CertificateInfoViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateInfoSerializer

    def get_queryset(self):
        return CertificateInfoModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class OtherCertificateInfoView(APIView):
    serializer_class = CertificateInfoSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = CertificateInfoModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"certificate_info": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class SkillsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = SkillsInfoSerializer

    def get_queryset(self):
        return SkillsInfoModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class OtherSkillsInfoView(APIView):
    serializer_class = SkillsInfoSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = SkillsInfoModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"skills_info": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class MajorProjectsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = MajorProjectsInfoSerializer
    search_fields = ['project_name']

    def get_queryset(self):
        return MajorProjectsInfoModel.objects.filter(user_profile=self.request.user.userprofilemodel)

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class OtherMajorProjectsInfoView(APIView):
    serializer_class = MajorProjectsInfoSerializer

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if user:
            user_profile = UserProfileModel.objects.filter(user=user).first()
            if user_profile:
                platforms = MajorProjectsInfoModel.objects.filter(user_profile=user_profile.pk)
                serializer = self.serializer_class(platforms, many=True)
                return Response({"certificate_info": serializer.data})
            else:
                return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
