from django.urls import path
from topTen import views
urlpatterns = [
    # path('front/', views.front_list),
    # path('front/<int:pk>/', views.stocks_detail),
    path('sector/', views.sector_view),
    path('home/', views.vTwo),

]