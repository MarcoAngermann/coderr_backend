from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'business_user', 'status', 'created_at', 'updated_at')
    search_fields = ('title', 'business_user__username')
    list_filter = ('status', 'created_at', 'updated_at')

admin.site.register(Order, OrderAdmin)

