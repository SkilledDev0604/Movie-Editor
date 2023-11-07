from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    product_view,
    preview_view
)

app_name = 'polls'

urlpatterns = [
    path('product/', product_view, name='product'),
    path('preview/', preview_view, name='preview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
