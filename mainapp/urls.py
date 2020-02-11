from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('contact-us/', contact_us, name="contact_us"),
    path('candidates/', home, name="candidates"),
    # detail for each candidate url



]
