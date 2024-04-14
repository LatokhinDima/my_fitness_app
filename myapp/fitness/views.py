from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from fitness.models import SportsCategory, SportsFacility, Service
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


def index(request):
    sports_facility_list = SportsFacility.objects.all()
    paginator = Paginator(sports_facility_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    SportsFacility.objects.prefetch_related(Service.__name__)
    return render(request, 'fitness/index.html', {'categories': sports_facility_list,
                                                  "page_obj": page_obj})

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
