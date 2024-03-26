from django.views.generic import ListView
from portfolioApi.models import CertificateInfoModel, EducationInfoModel, ExperienceInfoModel, MajorProjectsInfoModel, ProfileImageModel, ResumeUploadModel, SkillsInfoModel, SocialPlatformsModel, UserProfileModel

# Create your views here.
class DashboardView(ListView):
    template_name = 'dashboard.html'
    context_object_name = 'data'
    queryset = UserProfileModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['ProfileImage'] = ProfileImageModel.objects.all()
        context['ResumeUpload'] = ResumeUploadModel.objects.all()
        context['SocialPlatforms'] = SocialPlatformsModel.objects.filter(featured = True)
        context['EducationInfo'] = EducationInfoModel.objects.filter(featured = True).order_by('-start_date')
        context['ExperienceInfo'] = ExperienceInfoModel.objects.filter(featured = True).order_by('-start_date', 'currently_working')
        context['CertificateInfo'] = CertificateInfoModel.objects.filter(featured = True).order_by('-issue_date')
        context['SkillsInfo'] = SkillsInfoModel.objects.filter(featured = True).order_by('-proficiency', '-years_of_exp')
        context['MajorProjectsInfo'] = MajorProjectsInfoModel.objects.filter(featured = True).order_by('-currently_working')
        return context