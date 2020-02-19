import json

from django.contrib import messages
from django.core import serializers
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from Namzadan import settings

from .models import Candidate, City, Resume, Province


def home(request):
    all_candidates = Candidate.objects.filter(city__province__name__exact="تهران").order_by(
                    'resume', 'full_name')
    all_provinces = Province.objects.all().order_by('name')
    all_zones = City.objects.all().order_by('name')
    MEDIA_URL = settings.MEDIA_URL
    paginator = Paginator(all_candidates, 90)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET':
        selected_province = Province.objects.get(name__exact="تهران")
        return render(request, 'mainapp/all-candidates.html',
                      {'all_candidates': all_candidates, 'all_provinces': all_provinces, 'all_zones': all_zones,
                       'page_obj': page_obj, 'MEDIA_URL': MEDIA_URL, 'selected_province': selected_province})
    else:
        if 'search' in request.POST:
            search_text = str(request.POST['search'])
            all_candidates = Candidate.objects.filter(
                Q(full_name__contains=search_text) | Q(nickname__contains=search_text) |
                Q(father_name__contains=search_text) | Q(code__contains=search_text) |
                Q(party__contains=search_text) |
                Q(city__name__contains=search_text)).order_by(
                    'resume', 'full_name')
            paginator = Paginator(all_candidates, 90)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'mainapp/all-candidates.html',
                          {'all_candidates': all_candidates, 'all_provinces': all_provinces, 'all_zones': all_zones,
                           'MEDIA_URL': MEDIA_URL,
                           'page_obj': page_obj})
        province_pk = request.POST['province']
        zone_pk = request.POST['zone']
        if province_pk == "none":
            if zone_pk == "none":
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_provinces': all_provinces, 'all_zones': all_zones,
                               'MEDIA_URL': MEDIA_URL,
                               'page_obj': page_obj})
        if province_pk == "none":
            if zone_pk != "none":
                all_candidates = Candidate.objects.filter(city_id=zone_pk).order_by(
                    'resume', 'full_name')
                selected_zone = City.objects.get(pk=zone_pk)
                paginator = Paginator(all_candidates, 90)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_provinces': all_provinces, 'all_zones': all_zones,
                               'MEDIA_URL': MEDIA_URL,
                               'page_obj': page_obj, 'selected_zone': selected_zone})
        if province_pk != "none":
            if zone_pk == "none":
                all_candidates = Candidate.objects.filter(city__province_id=province_pk).order_by(
                    'resume', 'full_name')
                selected_province = Province.objects.get(pk=province_pk)
                paginator = Paginator(all_candidates, 90)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_provinces': all_provinces, 'all_zones': all_zones,
                               'MEDIA_URL': MEDIA_URL,
                               'page_obj': page_obj, 'selected_province': selected_province})
        if province_pk != "none":
            if zone_pk != "none":
                all_candidates = Candidate.objects.filter(city__province_id=province_pk, city_id=zone_pk).order_by(
                    'resume', 'full_name')
                selected_province = Province.objects.get(pk=province_pk)
                selected_zone = City.objects.get(pk=zone_pk)
                paginator = Paginator(all_candidates, 90)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_provinces': all_provinces, 'all_zones': all_zones,
                               'MEDIA_URL': MEDIA_URL,
                               'page_obj': page_obj, 'selected_province': selected_province,
                               'selected_zone': selected_zone})


def contact_us(request):
    return render(request, 'mainapp/AboutUs.html')


def resume(request, pk):
    MEDIA_URL = settings.MEDIA_URL
    try:
        resume = Resume.objects.get(candidate_id=pk)
    except:
        resume = None
    if resume is None:
        messages.error(request, "رزومه ای برای کاندیدای مورد نظر یافت نشد")
        return redirect('home')
    return render(request, 'mainapp/resume.html', {'resume': resume, 'MEDIA_URL': MEDIA_URL})


def get_cities(request):
    province_id = int(request.GET.get('province_id', None))
    cities = City.objects.filter(province_id=province_id).order_by('name')

    city_json = serializers.serialize('json', cities, fields=('name', 'pk'))

    data = {
        'city_json': city_json,
        'status': 200
    }
    from django.http import JsonResponse
    return JsonResponse(data)
