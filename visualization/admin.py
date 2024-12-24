from django.contrib import admin
from .models import RichPerson

@admin.register(RichPerson)
class RichPersonAdmin(admin.ModelAdmin):
    list_display = ('rank', 'name', 'total_net_worth', 'last_change', 'ytd_change', 'country_region', 'industry')
    search_fields = ('name', 'country_region', 'industry')
    list_filter = ('country_region', 'industry')
