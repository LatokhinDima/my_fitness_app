from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup/page/', views.index, name='index'),
    path('page/', views.index, name='index'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('service/<int:service_id>/', views.detail, name='detail'),
    path('services/<int:facility_id>/', views.get_services, name='get_services'),
    path('service/<int:service_id>/', views.add_to_cart, name='add_to_cart'),
    path('my_shopping_cart/', views.my_shopping_cart, name='my_shopping_cart'),
    path('shopping_cart_delete/', views.shopping_cart_delete, name='shopping_cart_delete'),
    path('make_order/', views.make_order, name='make_order'),
    path('profile/history/', views.profile_history_of_orders, name='profile_history_of_orders'),
    path('profile/<int:order_id>/', views.order_details, name='order_details'),

#    path('product/<int:product_id>/', views.detail, name='detail'),
#    path('category/<int:category_id>/', views.category, name='category'),
#    path('page/', views.index, name='index'),
#    path('signup/', views.signup, name='signup'),
#    path('signup/page/', views.index, name='index'),
#    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
#    path('my_shopping_cart/', views.my_shopping_cart, name='my_shopping_cart'),
#    path('shopping_cart_delete/', views.shopping_cart_delete, name='shopping_cart_delete'),
#    path('make_order/', views.make_order, name='make_order'),



]

