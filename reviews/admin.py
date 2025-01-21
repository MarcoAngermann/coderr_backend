from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'business_user', 'rating', 'created_at', 'updated_at')
    search_fields = ('reviewer__username', 'business_user__username')
    list_filter = ('rating', 'created_at')

admin.site.register(Review, ReviewAdmin)

