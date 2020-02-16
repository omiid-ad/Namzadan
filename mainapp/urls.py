from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('contact-us/', contact_us, name="contact_us"),
    path('candidates/', home, name="candidates"),
    path('resume/<int:pk>', resume, name="resume"),
    path('get_cities/', get_cities, name="get_cities"),

]
