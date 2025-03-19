"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include, re_path
from django.conf import settings
from django.templatetags.static import static
#from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # Используйте include() чтобы добавлять URL из каталога приложения
    path('ringer/', include('ringer.urls')),
    # Добавьте URL соотношения, чтобы перенаправить запросы 
    # с корневого URL, на URL приложения
    path('', RedirectView.as_view(url='/ringer/', permanent=True)),
    path('empty', RedirectView.as_view(url='', permanent=True)),
]

urlpatterns += [
    re_path(r'^ringer/static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^ringer/media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]


# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)