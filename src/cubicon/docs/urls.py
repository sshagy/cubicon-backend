import re

from django.urls import path, re_path
# from drf_yasg import openapi
# from drf_yasg.inspectors.view import SwaggerAutoSchema
# from drf_yasg.views import get_schema_view
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import APIRootView
from rest_framework.schemas import generators

# Monkey patching. Некоторый клстыль
if True:
    # def common_path(paths):
    #     """Определение общего префикса для всех эндпоинтов."""
    #     split_paths = [path.strip('/').split('/') for path in paths]
    #     s1 = min(split_paths)
    #     s2 = max(split_paths)
    #     common = s1
    #     # return '/' + '/'.join(common)
    #     return '/api/v1'

    # def get_tags(self, operation_keys=None):
    #     """Тег для каждого эндпоинта swagger auto doc"""
    #     tags = self.overrides.get('tags')
    #     if not tags:
    #         tags = [operation_keys[0]]
    #
    #     version = re.findall('/api/(v\d+)/', self.path)
    #     if version and version[0] != 'v1':
    #         tags[0] = f'{tags[0]}_{version[0]}'
    #
    #     return tags

    def get_tags(self):
        """ override this for custom behaviour """
        tokenized_path = self._tokenize_path()
        # use first non-parameter path part as tag
        # print(4444, tokenized_path)
        # return tokenized_path[:2]
        return ['api/v1']


    # generators.common_path = common_path
    # SwaggerAutoSchema.get_tags = get_tags
    AutoSchema.get_tags = get_tags

# schema_view = get_schema_view(
#     openapi.Info(
#         title="API",
#         default_version='v2',
#         description="Reference documentation for REST API endpoints",
#         terms_of_service="https://www.google.com/policies/terms/",
#         license=openapi.License(name="BSD License"),
#     ),
#     # validators=['flex', 'ssv'],
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    # re_path(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'),  name='redoc'),
    # path('drf/', include_docs_urls(
    #     title='Yet another documentation', authentication_classes=[], permission_classes=[])),
    re_path(r'^$', APIRootView.as_view(api_root_dict={
        # 'drf-doc': 'api-docs:docs-index',
        'swagger': 'swagger-ui',
        'redoc': 'redoc',
    }), name='docs_api_root'),
]
