from django.contrib import admin
from .models import SportsCategory, SportsFacility
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class SportsFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'address', 'category']
    search_fields = ['name']
    list_filter = ['name', 'category']


admin.site.register(SportsFacility, SportsFacilityAdmin)


class SportsFacilityInline(admin.TabularInline):
    model = SportsFacility
    extra = 1
    fields = ['name', 'description', 'address']


class SportsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    inlines = [SportsFacilityInline]


admin.site.register(SportsCategory, SportsCategoryAdmin)
