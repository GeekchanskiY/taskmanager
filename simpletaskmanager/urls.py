
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth', include("rest_framework.urls")),
    path('api/v1/taskmanager/', include('taskmanager.urls')),
    path('accounts/', include('rest_registration.api.urls'), name='register')
]
