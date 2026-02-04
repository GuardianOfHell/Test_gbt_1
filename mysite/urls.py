from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from mysite.views import *

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('production/', production, name='production'),
    path('Delivery-and-payment/', Delivery_and_payment, name='Delivery_and_payment'),
    path('project/', project, name='project'),
    path('catalog/', catalog, name='catalog'),
    path('Product_card/', Product_card, name='Product_card'),
    # path('news/', news, name='news'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
