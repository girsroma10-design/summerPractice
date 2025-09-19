from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('categories/', views.category_list, name='category_list'),
    path('create-category/', views.create_category, name='create_category'),
    path('create-category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.user_settings, name='settings'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)