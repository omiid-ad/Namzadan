from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Candidate, City, Zone


def home(request):
    all_candidates = Candidate.objects.all()
    all_cities = City.objects.all().order_by('name')
    all_zones = Zone.objects.all().order_by('city__name')
    paginator = Paginator(all_candidates, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET':
        return render(request, 'mainapp/all-candidates.html',
                      {'all_candidates': all_candidates, 'all_cities': all_cities, 'all_zones': all_zones,
                       'page_obj': page_obj})
    else:
        if 'search' in request.POST:
            search_text = str(request.POST['search'])
            all_candidates = Candidate.objects.filter(
                Q(full_name__contains=search_text) | Q(nickname__contains=search_text) |
                Q(father_name__contains=search_text) | Q(code__contains=search_text) |
                Q(party__contains=search_text) |
                Q(zone__city__name__contains=search_text))
            return render(request, 'mainapp/all-candidates.html',
                          {'all_candidates': all_candidates, 'all_cities': all_cities, 'all_zones': all_zones})
        city_pk = request.POST['city']
        zone_pk = request.POST['zone']
        if city_pk == "none":
            if zone_pk == "none":
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_cities': all_cities, 'all_zones': all_zones})
        if city_pk == "none":
            if zone_pk != "none":
                all_candidates = Candidate.objects.filter(zone_id=zone_pk)
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_cities': all_cities, 'all_zones': all_zones})
        if city_pk != "none":
            if zone_pk == "none":
                all_candidates = Candidate.objects.filter(zone__city_id=city_pk)
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_cities': all_cities, 'all_zones': all_zones})
        if city_pk != "none":
            if zone_pk != "none":
                all_candidates = Candidate.objects.filter(zone__city_id=city_pk, zone_id=zone_pk)
                return render(request, 'mainapp/all-candidates.html',
                              {'all_candidates': all_candidates, 'all_cities': all_cities, 'all_zones': all_zones})


def contact_us(request):
    return HttpResponse("contact us page")

# search views
