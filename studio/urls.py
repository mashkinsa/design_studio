from django.conf.urls.static import static
from django.urls import path
from design_studio import settings

from .views import index, login_view, register, profile, logout_view, main, create_request, view_requests, delete_request

urlpatterns = [
    path('', index, name='index'),
    path('main/', main, name='main'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('create/', create_request, name='create_request'),
    path('requests/', view_requests, name='view_requests'),
    path('requests/delete/<int:request_id>/', delete_request, name='delete_request'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)