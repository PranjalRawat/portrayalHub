# custom_filters.py
from django import template
from portfolioApi.models import EducationInfoModel, SocialPlatformsModel, ExperienceInfoModel, SkillsInfoModel, MajorProjectsInfoModel

register = template.Library()

@register.filter
def set_social_instance(form, social_id):
    social_platform_instance = SocialPlatformsModel.objects.get(id=social_id)
    updated_form = form.__class__(instance=social_platform_instance)
    return updated_form

@register.filter
def set_education_instance(form, education_id):
    education_info_instance = EducationInfoModel.objects.get(id=education_id)
    updated_form = form.__class__(instance=education_info_instance)
    return updated_form

@register.filter
def set_experience_instance(form, experience_id):
    experience_info_instance = ExperienceInfoModel.objects.get(id=experience_id)
    updated_form = form.__class__(instance=experience_info_instance)
    return updated_form

@register.filter
def set_skill_instance(form, skill_id):
    skill_info_instance = SkillsInfoModel.objects.get(id=skill_id)
    updated_form = form.__class__(instance=skill_info_instance)
    return updated_form

@register.filter
def set_project_instance(form, project_id):
    project_info_instance = MajorProjectsInfoModel.objects.get(id=project_id)
    updated_form = form.__class__(instance=project_info_instance)
    return updated_form
