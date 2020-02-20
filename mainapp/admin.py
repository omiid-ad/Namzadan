from django.contrib import admin
from django.contrib.auth.models import Group, User
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment

from .models import *


class CandidateA(admin.ModelAdmin):
    list_display = ('full_name', 'code', 'party', 'city')
    list_filter = ('city', 'party',)
    search_fields = ['code', 'full_name']
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
    list_display = ('name',)


class CityA(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)


class ResumeA(admin.ModelAdmin):
    list_display = ('candidate', 'age', 'degree',)
    list_filter = ('field', 'degree', 'candidate__city',)
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


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.unregister(Attachment)

admin.site.register(Candidate, CandidateC)
admin.site.register(Resume, ResumeC)
admin.site.register(Province, ProvinceA)
admin.site.register(City, CityA)
admin.site.register(GlobalAds)

admin.site.site_header = "نامزدان دات آی آر"
