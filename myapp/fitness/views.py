from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from fitness.models import SportsCategory, SportsFacility, Service
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


def index(request):
    sports_facility_list = SportsFacility.objects.all()
    sports_list = SportsCategory.objects.all()
    paginator = Paginator(sports_facility_list, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'fitness/index.html', {'categories': sports_facility_list,
                                                  "page_obj": page_obj, "sport_category": sports_list})


def category(request, category_id):
    sports_list = SportsCategory.objects.all()
    sport_category = get_object_or_404(SportsCategory, id=category_id)
    facilities = SportsFacility.objects.filter(category=category_id)
    context = {
        'facilities': facilities,
        'sport_category': sport_category,
        "sport_category_index": sports_list
    }
    return render(request, 'fitness/category.html', context)


def get_services(request, facility_id):
    facility = get_object_or_404(SportsFacility, id=facility_id)
    services = Service.objects.filter(facility=facility_id)
    context = {
        'services': services,
        'facility': facility
    }
    return render(request, 'fitness/get_services.html', context)

def detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'fitness/detail.html', {'service': service})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('page/')
    else:
        form = SignUpForm()
    return render(request, 'fitness/registration.html', {'form': form})
