from django.contrib import admin
from .models import Offer, OfferDetail

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0

class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username')
    list_filter = ('created_at', 'updated_at')
    inlines = [OfferDetailInline]

class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('offer', 'title', 'price', 'offer_type')
    search_fields = ('offer__title', 'title')
    list_filter = ('offer_type', 'price')

admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)

