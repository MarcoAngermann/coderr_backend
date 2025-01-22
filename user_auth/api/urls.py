from django.urls import path
from user_auth.api.views import Registration, Login, UserProfile, BusinessProfiles, CustomerProfiles

urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('profile/<int:id>/', UserProfile.as_view(), name='profile'),
    path('profiles/business/', BusinessProfiles.as_view(), name='business_profiles'),
    path('profiles/customer/', CustomerProfiles.as_view(), name='customer_profiles'),
]







