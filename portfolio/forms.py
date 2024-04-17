from django import forms
from portfolioApi.models import CertificateInfoModel, EducationInfoModel, ExperienceInfoModel, MajorProjectsInfoModel, ProfileImageModel, ResumeUploadModel, SkillsInfoModel, SocialPlatformsModel, UserProfileModel

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = '__all__'

class ProfileImageModelForm(forms.ModelForm):
    class Meta:
        model = ProfileImageModel
        fields = ['image']

class ResumeUploadModelForm(forms.ModelForm):
    class Meta:
        model = ResumeUploadModel
        fields = ['designation', 'cover_letter', 'resume', 'video_resume']

class SocialPlatformsModelForm(forms.ModelForm):
    class Meta:
        model = SocialPlatformsModel
        fields = ['platformName', 'platformIcon', 'profileUrl', 'featured']

class EducationInfoModelForm(forms.ModelForm):
    class Meta:
        model = EducationInfoModel
        fields = ['degree', 'university', 'start_date', 'end_date', 'university_logo', 'cgpa', 'featured']

class ExperienceInfoModelForm(forms.ModelForm):
    class Meta:
        model = ExperienceInfoModel
        fields = ['designation', 'company_name' , 'start_date', 'end_date', 'currently_working', 'company_logo', 'company_website', 'description',  'featured']

class CertificateInfoModelForm(forms.ModelForm):
    class Meta:
        model = CertificateInfoModel
        fields = ['course_name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_url', 'course_badge', 'featured']

class SkillsInfoModelForm(forms.ModelForm):
    class Meta:
        model = SkillsInfoModel
        fields = ['skill', 'years_of_exp', 'proficiency', 'skill_badge', 'featured']

class MajorProjectsInfoModelForm(forms.ModelForm):
    class Meta:
        model = MajorProjectsInfoModel
        fields = ['project_name', 'company_name', 'description', 'start_date', 'end_date', 'currently_working', 'project_url', 'project_logo', 'featured']
