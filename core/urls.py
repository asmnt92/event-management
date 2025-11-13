from django.urls import path
from .views import guest_view,features,contact_page

urlpatterns = [
    path('home/',guest_view,name='guest-page'),
    path('features/',features,name='features'),
    path('contact-us/',contact_page,name='contact')

]
