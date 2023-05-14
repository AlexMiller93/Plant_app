from django.contrib import admin

from .models import Plant

# Register your models here.

admin.site.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('title', 'latin_title', 'category', 'owner', 'appear_date')
    list_filter = ('category', 'latin_title', 'owner')
    search_fields = ('title', 'latin_title', 'category', 'owner')