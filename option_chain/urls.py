from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls', namespace='main')),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'