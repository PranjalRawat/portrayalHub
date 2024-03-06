from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from .models import SocialPlatformsModel, UserProfileModel, ProfileImageModel, ResumeUploadModel, EducationInfoModel, ExperienceInfoModel, CertificateInfoModel
from .serializers import SocialPlatformSerializer, UserProfileSerializer, UserProfileImageSerializer, ResumeUploadSerializer, EducationInfoSerializer, ExperienceInfoSerializer, CertificateInfoSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status

class SocialPlatformView(generics.ListCreateAPIView):
    queryset = SocialPlatformsModel.objects.all()
    serializer_class = SocialPlatformSerializer
    search_fields = ['platformName']
    ordering_fields = ['id']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class SocialPlatformDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocialPlatformsModel.objects.all()
    serializer_class = SocialPlatformSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def patch(self, request, *args, **kwargs):
        queryset = SocialPlatformsModel.objects.get(pk=self.kwargs['pk'])
        queryset.featured = not queryset.featured
        queryset.save()
        return JsonResponse(status=200, data={'message':'Featured status of {} changed to {}'.format(str(queryset.title), str(queryset.featured))})

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfileModel.objects.all()

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
    queryset = ProfileImageModel.objects.all()

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
    queryset = ResumeUploadModel.objects.all()

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
    queryset = EducationInfoModel.objects.all()
    serializer_class = EducationInfoSerializer
    search_fields = ['degree', 'university']
    ordering_fields = ['cgpa', 'end_date']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

class ExperienceInfoViewSet(viewsets.ModelViewSet):
    queryset = ExperienceInfoModel.objects.all()
    serializer_class = ExperienceInfoSerializer
    search_fields = ['company_name', 'designation']
    ordering_fields = ['end_date']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        currently_working = self.request.data.get('currently_working', False)

        if currently_working and ExperienceInfoModel.objects.filter(currently_working=True).exists():
            return Response({'detail': 'Only one instance can have currently_working as True.'}, status=400)

        if currently_working:
            instance.end_date = None
            instance.save()


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
    queryset = CertificateInfoModel.objects.all()
    serializer_class = CertificateInfoSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
