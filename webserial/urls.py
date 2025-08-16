from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('sercon/', include('sercon.urls')),
    path('admin/', admin.site.urls),
]
