from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.models import User 

class Order(models.Model):
    STATUS_CHOICES = [
        ('cancelled', 'Cancelled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    offer_detail_id = models.ForeignKey(
        "offers.OfferDetail",
        verbose_name=_("OfferDetail"),
        on_delete=models.CASCADE
    )
    customer_user = models.IntegerField(default=0)
    business_user = models.ForeignKey(
        User, 
        verbose_name=_("Business User"),
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(null=True, blank=True)
    delivery_time_in_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    features = models.JSONField(null=True, blank=True)
    offer_type = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.business_user_id and self.offer_detail_id:
            self.business_user = self.offer_detail_id.offer.user
        if not self.title and self.offer_detail_id:
            self.title = self.offer_detail_id.title
        if self.offer_detail_id:
            self.revisions = self.revisions or self.offer_detail_id.revisions
            self.delivery_time_in_days = self.delivery_time_in_days or self.offer_detail_id.delivery_time_in_days
            self.price = self.price or self.offer_detail_id.price
            self.features = self.features or self.offer_detail_id.features
            self.offer_type = self.offer_type or self.offer_detail_id.offer_type
        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.updated_at = now()
        super().save(*args, **kwargs)