from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/', null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OfferDetail(models.Model):
    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.IntegerField(default=1)
    price = models.FloatField(default=1)
    features = models.JSONField()
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES)

    def save(self, *args, **kwargs):
            
            if self.price is not None:
                self.price = round(self.price, 2)  # Auf 2 Nachkommastellen runden
            super().save(*args, **kwargs)
