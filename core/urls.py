from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from menu.views import home_page, create_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('create-order/', create_order, name='create_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)