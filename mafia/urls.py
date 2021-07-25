from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from mafia import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)