from django.conf.urls.static import static
from django.urls import path
from design_studio import settings

from .views import (index, login_view, register, profile, logout_view, main, create_request, view_requests,
                    delete_request, admin_design_requests, admin_categories, create_category, edit_category, delete_category)

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
    path('admin/design-requests/', admin_design_requests, name='admin_design_requests'),
    path('categories/', admin_categories, name='admin_categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)