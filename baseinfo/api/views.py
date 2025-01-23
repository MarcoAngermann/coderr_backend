from rest_framework.views import APIView
from rest_framework.response import Response
from reviews.models import Review
from user_auth.models import Profile
from offers.models import Offer 
from django.db.models import Avg

class BaseInfoViews(APIView):
    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(average_rating=Avg('rating'))['average_rating']
        average_rating = round(average_rating, 1) if average_rating is not None else 0
        business_profile_count = Profile.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data)
