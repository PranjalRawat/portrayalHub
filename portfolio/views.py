import json
from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, UpdateView, CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from portfolio.forms import CertificateInfoModelForm, ContactForm, EducationInfoModelForm, ExperienceInfoModelForm, MajorProjectsInfoModelForm, ProfileImageModelForm, ResumeUploadModelForm, ResumeUploadUpdateModelForm, SkillsInfoModelForm, SocialPlatformsModelForm, UserProfileModelForm
from portfolioApi.models import CertificateInfoModel, EducationInfoModel, ExperienceInfoModel, MajorProjectsInfoModel, ProfileImageModel, ResumeUploadModel, SkillsInfoModel, SocialPlatformsModel, UserProfileModel
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from portrayalHub.settings import Email_from, Email_to
from django.contrib.auth.models import User

# Create your views here.
class DashboardView(DetailView):
    template_name = 'dashboard.html'
    user_not_found_template = 'user_not_found.html'
    user_not_authenticated_template = 'user_not_authenticated.html'
    context_object_name = 'data'
    form_class = ContactForm

    def get_object(self):
        username = self.kwargs.get('username')
        if not username:
            if self.request.user.is_authenticated:
                return User.objects.get(username=self.request.user)
            return None
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            None

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        if not request.user.is_authenticated and not username:
            return render(request, self.user_not_authenticated_template, status=401)
        user = self.get_object()
        if not user:  # If user is not found, render user_not_found.html
            return render(request, self.user_not_found_template, status=404)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            message = 'From - '+name+'\nEmail Address - '+email+'\n\n'+message
            send_mail(
                subject,
                message,
                Email_from,
                [Email_to],
            )
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        context['UserProfile'] = UserProfileModel.objects.filter(user=user)
        context['ProfileImage'] = ProfileImageModel.objects.filter(user_profile=user_profile)
        context['ResumeUpload'] = ResumeUploadModel.objects.filter(user_profile=user_profile)
        context['SocialPlatforms'] = SocialPlatformsModel.objects.filter(user_profile=user_profile, featured = True)
        context['EducationInfo'] = EducationInfoModel.objects.filter(user_profile=user_profile, featured = True).order_by('-start_date')
        context['ExperienceInfo'] = ExperienceInfoModel.objects.filter(user_profile=user_profile, featured = True).order_by('-start_date', 'currently_working')
        context['CertificateInfo'] = CertificateInfoModel.objects.filter(user_profile=user_profile, featured = True).order_by('-issue_date')
        context['SkillsInfo'] = SkillsInfoModel.objects.filter(user_profile=user_profile, featured = True).order_by('-proficiency', '-years_of_exp')
        context['MajorProjectsInfo'] = MajorProjectsInfoModel.objects.filter(user_profile=user_profile, featured = True).order_by('-currently_working')
        context['contacts'] = ContactForm
        return context

class PageNotFoundView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        return render(request, '404.html', status=404)

class LogInView(LoginView):
    template_name = 'registration/login.html'

class LogOutView(LogoutView):
    template_name = 'registration/logout_success.html'

class ProfileEditView(TemplateView):
    template_name = 'profile.html'
    user_not_authenticated_template = 'user_not_authenticated.html'
    context_object_name = 'data'

    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.user_not_authenticated_template, status=401)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        context['UserProfile'] = UserProfileModel.objects.filter(user=user)
        context['ProfileImage'] = ProfileImageModel.objects.filter(user_profile=user_profile)
        context['ResumeUpload'] = ResumeUploadModel.objects.filter(user_profile=user_profile)
        context['SocialPlatforms'] = SocialPlatformsModel.objects.filter(user_profile=user_profile)
        context['EducationInfo'] = EducationInfoModel.objects.filter(user_profile=user_profile).order_by('-start_date')
        context['ExperienceInfo'] = ExperienceInfoModel.objects.filter(user_profile=user_profile)
        context['SkillsInfo'] = SkillsInfoModel.objects.filter(user_profile=user_profile)
        context['MajorProjectsInfo'] = MajorProjectsInfoModel.objects.filter(user_profile=user_profile)
        context['CertificateInfo'] = CertificateInfoModel.objects.filter(user_profile=user_profile)

        # Populate forms with data from the first instance for each model
        context['user_profile_form'] = UserProfileModelForm(instance=user_profile)
        context['profile_image_form'] = ProfileImageModelForm(instance=context['ProfileImage'].first())
        context['resume_upload_form'] = ResumeUploadModelForm(instance=ResumeUploadModel.objects.first())
        context['resume_upload_update_form'] = ResumeUploadUpdateModelForm(instance=ResumeUploadModel.objects.first())
        context['social_platforms_form'] = SocialPlatformsModelForm(user_profile = user_profile)
        context['education_info_form'] = EducationInfoModelForm(user_profile = user_profile)
        context['experience_info_form'] = ExperienceInfoModelForm(user_profile = user_profile)
        context['skills_info_form'] = SkillsInfoModelForm(user_profile = user_profile)
        context['certificate_info_form'] = CertificateInfoModelForm(instance=CertificateInfoModel.objects.first())
        context['major_projects_info_form'] = MajorProjectsInfoModelForm(instance=MajorProjectsInfoModel.objects.first())

        context['user_profile_action_url'] = reverse_lazy('updateProfileView', kwargs={'pk': user_profile.pk})
        context['user_profile_image_action_url'] = reverse_lazy('updateProfileImageView', kwargs={'pk': user_profile.pk})
        context['user_resume_upload_action_url'] = reverse_lazy('updateResumeUploadView', kwargs={'pk': user_profile.pk})
        context['create_social_platform_action_url'] = reverse_lazy('createSocialPlatformView')
        context['create_education_info_action_url'] = reverse_lazy('createEducationInfoView')
        context['create_experience_info_action_url'] = reverse_lazy('createExperienceInfoView')
        context['create_skill_info_action_url'] = reverse_lazy('createSkillsInfoView')


        return context

class UpdateProfileView(UpdateView):

    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['instance'] = user_profile
        return kwargs

    form_class = UserProfileModelForm
    success_url = '/profile'

class UpdateProfileImageView(UpdateView):
    queryset = ProfileImageModel.objects.all()
    form_class = ProfileImageModelForm
    success_url = '/profile'

class UpdateResumeUploadView(UpdateView):
    queryset = ResumeUploadModel.objects.all()
    form_class = ResumeUploadUpdateModelForm
    success_url = '/profile'

class CreateSocialPlatformView(CreateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        return kwargs

    form_class = SocialPlatformsModelForm
    success_url = '/profile#social'

class DeleteSocialPlatformView(DeleteView):
    model = SocialPlatformsModel
    success_url = '/profile#social'

    def dispatch(self, request, *args, **kwargs):
        # Directly delete the object without displaying the confirmation page
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

class UpdateSocialPlatformView(UpdateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        instance_id = self.kwargs.get('pk')
        kwargs['instance'] = SocialPlatformsModel.objects.get(id=instance_id)
        return kwargs

    form_class = SocialPlatformsModelForm
    success_url = '/profile#social'

class CreateEducationInfoView(CreateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        return kwargs

    form_class = EducationInfoModelForm
    success_url = '/profile#education'

class DeleteEducationInfoView(DeleteView):
    model = EducationInfoModel
    success_url = '/profile#education'

    def dispatch(self, request, *args, **kwargs):
        # Directly delete the object without displaying the confirmation page
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

class UpdateEducationInfoView(UpdateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        instance_id = self.kwargs.get('pk')
        kwargs['instance'] = EducationInfoModel.objects.get(id=instance_id)
        return kwargs

    form_class = EducationInfoModelForm
    success_url = '/profile#education'

class CreateExperienceInfoView(CreateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        return kwargs

    form_class = ExperienceInfoModelForm
    success_url = '/profile#experience'

class DeleteExperienceInfoView(DeleteView):
    model = ExperienceInfoModel
    success_url = '/profile#experience'

    def dispatch(self, request, *args, **kwargs):
        # Directly delete the object without displaying the confirmation page
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

class UpdateExperienceInfoView(UpdateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        instance_id = self.kwargs.get('pk')
        kwargs['instance'] = ExperienceInfoModel.objects.get(id=instance_id)
        return kwargs

    form_class = ExperienceInfoModelForm
    success_url = '/profile#experience'

class CreateSkillsInfoView(CreateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        return kwargs

    form_class = SkillsInfoModelForm
    success_url = '/profile#skills'

class DeleteSkillsInfoView(DeleteView):
    model = SkillsInfoModel
    success_url = '/profile#skills'

    def dispatch(self, request, *args, **kwargs):
        # Directly delete the object without displaying the confirmation page
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)

class UpdateSkillsInfoView(UpdateView):
    def get_object(self):
        if self.request.user.is_authenticated:
            return User.objects.get(username=self.request.user)
        return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Get the user profile instance and pass it to the form
        user = self.get_object()
        user_profile = UserProfileModel.objects.get(user=user)
        kwargs['user_profile'] = user_profile
        instance_id = self.kwargs.get('pk')
        kwargs['instance'] = SkillsInfoModel.objects.get(id=instance_id)
        return kwargs

    form_class = SkillsInfoModelForm
    success_url = '/profile#skills'
