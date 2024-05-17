# custom_filters.py
from django import template
from portfolioApi.models import EducationInfoModel, SocialPlatformsModel

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
