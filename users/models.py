from django.db import models

class User(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    )
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=USER_TYPES)

    class Meta:
        abstract = True

class Customer(User):
    address = models.CharField(max_length=255)

class Provider(User):
    company_name = models.CharField(max_length=255)



