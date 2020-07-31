from django.contrib import admin
from django.contrib.auth.models import Group, User
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment

from .models import *


class CandidateA(admin.ModelAdmin):
    list_display = ('full_name', 'get_profile_picture', 'code', 'party', 'city', 'get_resume')
    list_filter = ('party',)
    search_fields = ['code', 'full_name', 'city__name']
    fieldsets = (
        (None, {
            'fields': (('full_name', 'father_name', 'code', 'party', 'city'), 'profile_picture_url')
        }),
        ('اطلاعات بیشتر', {
            'classes': ('collapse',),
            'fields': ('nickname', 'motto')
        }),
    )


class CandidateB(SummernoteModelAdmin):
    summernote_fields = '__all__'


class CandidateC(CandidateA, CandidateB):
    pass


class ProvinceA(admin.ModelAdmin):
    list_display = ('name', 'get_city_count')
    search_fields = ['name', ]


class CityA(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)
    search_fields = ['name', 'province__name']


class ResumeA(admin.ModelAdmin):
    list_display = ('candidate', 'age', 'degree', 'get_truncated_moarefi_barnameha')
    list_filter = ('field', 'degree',)
    search_fields = ['candidate__full_name', 'candidate__code']
    fieldsets = (
        (None, {
            'fields': (
                ('candidate', 'age', 'degree', 'field'), ('moarefi_barnameha', 'records'), 'banner1')
        }),
        ('پوسترهای بیشتر', {
            'classes': ('collapse',),
            'fields': ('banner2', 'banner3', 'banner4')
        }),
    )


class ResumeB(SummernoteModelAdmin):
    summernote_fields = '__all__'


class ResumeC(ResumeA, ResumeB):
    pass


class GlobalAdsA(admin.ModelAdmin):
    list_display = ('candidate', 'get_banner_thumb')
    search_fields = ['candidate__full_name', 'candidate__code']


admin.site.unregister(Group)
# admin.site.unregister(User)
admin.site.unregister(Attachment)

admin.site.register(Candidate, CandidateC)
admin.site.register(Resume, ResumeC)
admin.site.register(Province, ProvinceA)
admin.site.register(City, CityA)
admin.site.register(GlobalAds, GlobalAdsA)
