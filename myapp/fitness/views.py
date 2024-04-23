from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import SportsCategory, SportsFacility, Service, Profile, OrderEntry, Order, Status
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


def profile_cart_init(user):
    profile: Profile = Profile.objects.get_or_create(user=user)[0]
    if not profile.shopping_cart:
        profile.shopping_cart = (profile.orders.filter(status=Status.INITIAL).first()
                                 or Order.objects.create(profile=profile, status=Status.INITIAL))
        profile.save()

    return profile.shopping_cart


# @login_required
# def add_to_cart(request, service_id):
#     service = get_object_or_404(Service, id=service_id)
#     current_order = profile_cart_init(request.user)
#     entry = OrderEntry.objects.get_or_create(order=current_order,
#                                              service=service)[0]
#     entry.count += 1
#     entry.save()
#     return redirect('fitness:detail', service_id)

@login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    current_order = profile_cart_init(request.user)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        entry, created = OrderEntry.objects.get_or_create(order=current_order, service=service)
        entry.start_date = start_date
        entry.end_date = end_date
        entry.save()
    else:
        entry, created = OrderEntry.objects.get_or_create(order=current_order, service=service)
        entry.start_date = datetime.date.today()
        entry.end_date = entry.start_date + timedelta(days=30)
        entry.save()
    return redirect('fitness:detail', service_id)


# @login_required
# def add_to_cart(request: HttpRequest):
#     if request.method == 'POST':
#         service_id = int(request.POST['service_id'])
#         service = get_object_or_404(Service, id=service_id)
#
#         start_date_str = request.POST.get('start_date')
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else timezone.now().date()
#
#         shopping_cart: Order = request.user.profile.shopping_cart
#         target_order_entry: OrderEntry = shopping_cart.order_entries.filter(service=service).first()
#
#         if not target_order_entry:
#             end_date = start_date + timezone.timedelta(days=30)
#             target_order_entry = shopping_cart.order_entries.create(service=service, start_date=start_date, end_date=end_date)
#             target_order_entry.save()
#
#     return redirect('fitness:detail', service_id)


@login_required
def my_shopping_cart(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()
    if (not profile.shopping_cart) or len(profile.shopping_cart.order_entries.all()) == 0:
        return render(request, 'fitness/my_shopping_cart.html')

    entries = profile.shopping_cart.order_entries.all().order_by('-id')
    total_price = sum([entry.service.price for entry in entries])
    return render(request, 'fitness/my_shopping_cart.html', {'entries': entries,
                                                             'total_price': total_price})


@login_required
def shopping_cart_delete(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    if profile.shopping_cart:
        profile.shopping_cart.delete()

    return redirect('fitness:my_shopping_cart')


@login_required
def make_order(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()

    order = profile.shopping_cart
    order.status = Status.COMPLETED
    order.save()

    profile.shopping_cart = None
    profile.save()

    return render(request, 'fitness/make_order.html')


@login_required()
def profile_history_of_orders(request):
    profile: Profile = Profile.objects.filter(user=request.user).first()
    orders = profile.orders.exclude(status=Status.INITIAL).order_by('-id')

    context = {
        'profile': profile,
        'orders': orders,
    }

    return render(request, 'fitness/history_of_orders.html', context)


@login_required()
def order_details(request, order_id: int):
    profile: Profile = Profile.objects.filter(user=request.user).first()
    order: Order = Order.objects.filter(id=order_id).first()
    entries = []
    for entry in order.order_entries.all().order_by('id'):
        entries.append(entry)
    context = {
        'order': order,
        'profile': profile,
        'entries': entries,
    }
    return render(request, 'fitness/order_detail.html', context)
