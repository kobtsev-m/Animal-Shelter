from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from django.views.static import serve


handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'


urlpatterns = [
    path('', include('main.urls')),
    path('gallery/', include('gallery.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.extend([
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ])