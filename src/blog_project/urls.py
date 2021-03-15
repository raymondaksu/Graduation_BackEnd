from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('user/', include('user.urls')),
    # path('chat/', include('chat.urls')),
    path('nested-admin/', include('nested_admin.urls')),
    path('auth/', include('dj_rest_auth.urls')),
]
