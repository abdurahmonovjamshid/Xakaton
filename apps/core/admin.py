from django.contrib import admin

from .models import District, Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    list_filter = ['region']
    ordering = ['name']
