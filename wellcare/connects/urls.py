from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('check/', views.CheckPage.as_view(), name="check"),
    path('check/showcheck/', views.ShowCheckPage.as_view(), name="showcheck"),
    path('service-first/', views.ServiceFirst.as_view(), name="service-first"),
    path('service-1/', views.ServiceFirst1.as_view(), name="service-1"),
    path('service-2/', views.ServiceFirst2.as_view(), name="service-2"),
    path('service-3/', views.ServiceFirst3.as_view(), name="service-3"),
    path('service-4/', views.ServiceFirst4.as_view(), name="service-4"),

    path('service-sec/', views.ServiceSecond.as_view(), name="service-sec"),
    path('second-1/', views.ServiceSecond1.as_view(), name="second-1"),
    path('second-2/', views.ServiceSecond2.as_view(), name="second-2"),
    path('second-3/', views.ServiceSecond3.as_view(), name="second-3"),
    path('second-4/', views.ServiceSecond4.as_view(), name="second-4"),

    path('service-third/', views.ServiceThird.as_view(), name="service-third"),
    path('third-1/', views.ServiceThird1.as_view(), name="third-1"),
    path('third-2/', views.ServiceThird2.as_view(), name="third-2"),
    path('third-3/', views.ServiceThird3.as_view(), name="third-3"),
    path('third-4/', views.ServiceThird4.as_view(), name="third-4"),
    
]
