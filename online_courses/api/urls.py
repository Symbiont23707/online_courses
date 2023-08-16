from django.urls import path, include
from api import auth

urlpatterns = [
    path('auth/', include(auth.urlpatterns)),
    path('v1/', include('api.v1.urls')),
]
