from rest_framework.routers import DefaultRouter
from django.urls import path , include 
from .views import SessionViewSet
route = DefaultRouter()
route.register('session',SessionViewSet)




urlpatterns = [
    path('',include(route.urls)),
    
]
