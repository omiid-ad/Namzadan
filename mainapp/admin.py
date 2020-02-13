from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import *


class CandidateA(admin.ModelAdmin):
    list_display = ('full_name', 'code', 'party', 'zone')
    list_filter = ('zone', 'party',)
    search_fields = ['code', 'full_name']
    fieldsets = (
        (None, {
            'fields': (('full_name', 'father_name', 'code', 'party', 'zone'), 'profile_picture_url')
        }),
        ('اطلاعات بیشتر', {
            'classes': ('collapse',),
            'fields': ('nickname', 'motto')
        }),
    )


# class ResumeA(admin.ModelAdmin):
#     list_display = ('full_name', 'code', 'party', 'zone')


class ProvinceA(admin.ModelAdmin):
    list_display = ('name',)


class CityA(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)


class ZoneA(admin.ModelAdmin):
    list_display = ('name', 'city',)
    list_filter = ('city',)


class ResumeA(admin.ModelAdmin):
    list_display = ('candidate', 'age', 'degree',)
    list_filter = ('field', 'degree', 'candidate__zone',)
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


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Candidate, CandidateA)
admin.site.register(Resume, ResumeA)
admin.site.register(Province, ProvinceA)
admin.site.register(City, CityA)
admin.site.register(Zone, ZoneA)

admin.site.site_header = "نامزدان دات آی آر"
