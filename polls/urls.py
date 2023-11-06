from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    page_view
)

app_name = 'polls'

urlpatterns = [
    path('', page_view, name='polls'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
