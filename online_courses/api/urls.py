from django.contrib import admin
from django.urls import path, include

from api import auth
from api import v1

urlpatterns = [
    path('auth/', include(auth.urlpatterns)),
    path('v1/', include('api.v1.urls')),
]
