from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    product_view,
    preview_view,
    for_redirect
)

app_name = 'polls'

urlpatterns = [
    path('preview/', preview_view, name='preview'),
    path('product/<int:index>/', product_view, name ='product'),
    path('product/', for_redirect, name='product_redirect'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
