from django.conf.urls.static import static
from django.urls import path
from design_studio import settings

from .views import index, login_view, register, profile, logout_view
urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)