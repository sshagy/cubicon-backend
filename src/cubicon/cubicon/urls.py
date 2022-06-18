"""cubicon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings

from .views import get_api_navigation, get_api_root_view, AboutViewSet


admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include('docs.urls')),
    # path('api/v1/logs/', include('models_logging.api.urls')),
    path('api/v1/about/', AboutViewSet.as_view({'get': 'version'}), name='about-version'),
    # path('api/v1/health/', views.HealthView.as_view(
    #     authentication_classes=[], permission_classes=[]), name='Application health'),

    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/events/', include('events.urls')),
]


if settings.DEBUG:
    from django.apps import apps
    from django.conf.urls.static import static
    # urlpatterns += (
    #     static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
    #     static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # )
    if apps.is_installed('silk'):
        urlpatterns += [path('silk/', include('silk.urls'))]
    if apps.is_installed('debug_toolbar'):
        # import debug_toolbar
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]


# добавляем навигацию для эндпоинтов `/, /api/, /api/v1|v2/`
urlpatterns += [
    path(r'api/v1/',
         get_api_root_view(
             api_root_dict={

                # **get_api_navigation(urlpatterns)
                 # 'v1': 'api-root-v1',
                 # 'v2': 'api-root-v2',
             },
             verbose_name='Versions API'
         ),
         name='api-root-versions'),
# path('api/v1/',
#          get_api_root_view(api_root_dict=get_api_navigation(urlpatterns, pattern='api/v1/'), verbose_name='V1'),
#          name='api-root-v1'),
]
urlpatterns += [
    re_path(r'^$',
            get_api_root_view(
                api_root_dict={
                    **get_api_navigation(urlpatterns),
                    'admin': 'admin:index',
                    'docs': 'docs_api_root',
                    # 'api': 'api-root-versions',
                },
                verbose_name='Root'),
            name='api-root-main'),
    # path('api/v1/',
    #      get_api_root_view(api_root_dict=get_api_navigation(urlpatterns, pattern='api/v1/'), verbose_name='V1'),
    #      name='api-root-v1'),
    # path('api/v2/',
    #      get_api_root_view(api_root_dict=get_api_navigation(urlpatterns, pattern='api/v2/'), verbose_name='V2'),
    #      name='api-root-v2'),
]
print(1111, urlpatterns)

