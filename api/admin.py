from django.contrib import admin

from api.models import Fish
class FishAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name',)
admin.site.register(Fish, FishAdmin)
