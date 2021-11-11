from django.urls import path
from core.views import *
from core.views.health_check import HealthCheckView

urlpatterns = [
    path('games', GameAPIView.as_view()),
    path('games/addprice', GameAPIPriceView.as_view()),
    path('check', HealthCheckView.as_view())
]
