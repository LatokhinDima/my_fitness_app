from django.contrib import admin
from .models import SportsCategory, SportsFacility, Service
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1
    fields = ['name', 'description', 'price']


class SportsFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'address', 'picture', 'get_categories']
    search_fields = ['name']
    list_filter = ['name', 'category']
    filter_horizontal = ['category']
    inlines = [ServiceInline]

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])

    get_categories.short_description = 'Categories'


admin.site.register(SportsFacility, SportsFacilityAdmin)


class SportsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


admin.site.register(SportsCategory, SportsCategoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'facility']
    search_fields = ['name']
    list_filter = ['name', 'price', 'facility']


admin.site.register(Service, ServiceAdmin)
