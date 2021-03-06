
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
import django.views.defaults

app_name = 'main'

urlpatterns = [
    path('',views.MyLoginView.as_view(), name='login'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('fii_dii/',views.fii_dii,name='fii_dii'),
    path('optionchain/',views.optionchain,name='optionchain'),
    path('events/',views.events,name='events'),
    path('blockdeals/',views.block_deals,name='block_deals'),
    path('news/',views.news,name='news'),
    path('logout/',auth_views.LogoutView.as_view(template_name='main/accounts/logout.html'),name='logout'),
    path('search/', views.requestSearch, name='search'),
    path('stock_info/<str:stock_name>/',views.stock_info, name='stock_info'),
]

