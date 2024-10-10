from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('check/', views.CheckPage.as_view(), name="check"),
    path('check/showcheck/', views.ShowCheckPage.as_view(), name="showcheck"),
    
]
