from django.contrib import admin
from .models import SportsCategory, SportsFacility, Service, Order, OrderEntry, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

class ProfileAdmin(admin.ModelAdmin):
    inlines = [OrderInline]



class OrderEntryInline(admin.TabularInline):
    model = OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderEntryInline]

class OrderEntryAdmin(admin.ModelAdmin):
    pass

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(OrderEntry, OrderEntryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
