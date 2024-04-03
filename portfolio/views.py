from django.views.generic import DetailView
from portfolio.forms import ContactForm
from portfolioApi.models import CertificateInfoModel, EducationInfoModel, ExperienceInfoModel, MajorProjectsInfoModel, ProfileImageModel, ResumeUploadModel, SkillsInfoModel, SocialPlatformsModel, UserProfileModel
from django.shortcuts import redirect
from django.core.mail import send_mail
from portrayalHub.settings import Email_from, Email_to
from django.contrib.auth.models import User
from django.http import Http404

# Create your views here.
class DashboardView(DetailView):
    template_name = 'dashboard.html'
    context_object_name = 'data'
    queryset = UserProfileModel.objects.all()
    form_class = ContactForm
    slug_field = 'user'
    slug_url_kwarg = 'username'

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

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        return user

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['UserProfile'] = UserProfileModel.objects.all()
        context['ProfileImage'] = ProfileImageModel.objects.all()
        context['ResumeUpload'] = ResumeUploadModel.objects.all()
        context['SocialPlatforms'] = SocialPlatformsModel.objects.filter(featured = True)
        context['EducationInfo'] = EducationInfoModel.objects.filter(featured = True).order_by('-start_date')
        context['ExperienceInfo'] = ExperienceInfoModel.objects.filter(featured = True).order_by('-start_date', 'currently_working')
        context['CertificateInfo'] = CertificateInfoModel.objects.filter(featured = True).order_by('-issue_date')
        context['SkillsInfo'] = SkillsInfoModel.objects.filter(featured = True).order_by('-proficiency', '-years_of_exp')
        context['MajorProjectsInfo'] = MajorProjectsInfoModel.objects.filter(featured = True).order_by('-currently_working')
        context['contacts'] = ContactForm
        return context
