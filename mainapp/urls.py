from django.urls import path
from .views import *

urlpatterns = [
    path('landing/', home, name="home"),
    path('', home, name="home"),
    path('contact-us/', contact_us, name="contact_us"),
    path('candidates/', candidates, name="candidates"),
    # detail for each candidate url



]
