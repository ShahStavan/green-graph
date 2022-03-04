from main.views import error_404,error_500
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls', namespace='main')),
]

handler404 = error_404
handler500 = error_500