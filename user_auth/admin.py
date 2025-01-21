from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'username', 'type', 'created_at')
    search_fields = ('user__username', 'email', 'username')
    list_filter = ('type', 'created_at')

admin.site.register(Profile, ProfileAdmin)

