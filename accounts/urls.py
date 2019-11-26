from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_check, name='login'),
    path('logout/', logout, name='logout'),
    path('follow/', follow, name='follow'),
]