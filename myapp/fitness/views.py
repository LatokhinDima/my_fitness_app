from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from fitness.models import SportsCategory, SportsFacility, Service
from django.contrib.auth import login, authenticate
#from .forms import SignUpForm

def index(request):
    sports_facility_list = SportsFacility.objects.all()
    paginator = Paginator(sports_facility_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    SportsFacility.objects.prefetch_related(Service.__name__)
    return render(request, 'fitness/index.html', {'categories': sports_facility_list, "page_obj": page_obj})
