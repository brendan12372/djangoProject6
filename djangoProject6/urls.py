
from django.urls import path, include

urlpatterns = [
    path("topTen/", include('topTen.urls'))
]