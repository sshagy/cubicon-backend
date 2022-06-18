"""
Django Settings for auto-generated documentation systems.

See https://www.django-rest-framework.org/topics/documenting-your-api/#third-party-packages

TODO: Integrated
1. https://github.com/manosim/django-rest-framework-docs
2. https://github.com/iMakedonsky/drf-autodocs
3. https://shhaggy.docs.apiary.io/#
"""

# Настройки генераторов документации
SPECTACULAR_SETTINGS = {
    'TITLE': 'Cubicon API',
    'DESCRIPTION': 'Description of Cubicon project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    # OTHER SETTINGS
}
# SWAGGER_SETTINGS = {
#     # default inspector classes, see advanced documentation
#     'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
#     # 'DEFAULT_FIELD_INSPECTORS': [
#     #     'drf_yasg.inspectors.CamelCaseJSONFilter',
#     #     'drf_yasg.inspectors.ReferencingSerializerInspector',
#     #     'drf_yasg.inspectors.RelatedFieldInspector',
#     #     'drf_yasg.inspectors.ChoiceFieldInspector',
#     #     'drf_yasg.inspectors.FileFieldInspector',
#     #     'drf_yasg.inspectors.DictFieldInspector',
#     #     'drf_yasg.inspectors.SimpleFieldInspector',
#     #     'drf_yasg.inspectors.StringDefaultFieldInspector',
#     # ],
#     # 'DEFAULT_FILTER_INSPECTORS': [
#     #     'drf_yasg.inspectors.CoreAPICompatInspector',
#     # ],
#     'DEFAULT_PAGINATOR_INSPECTORS': [
#         'drf_yasg.inspectors.DjangoRestResponsePagination',
#         'drf_yasg.inspectors.CoreAPICompatInspector',
#     ],
#
#     # default api Info if none is otherwise given;
#     # should be an import string to an openapi.Info object
#     'DEFAULT_INFO': None,
#     # default API url if none is otherwise given
#     'DEFAULT_API_URL': None,
#
#     # add Django Login and Django Logout buttons, CSRF token to swagger UI page
#     'USE_SESSION_AUTH': True,
#     'LOGIN_URL': '/api-auth/login/',  # URL for the login button
#     'LOGOUT_URL': '/api-auth/logout/',  # URL for the logout button
#
#     # Swagger security definitions to include in the schema;
#     # see https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#security-definitions-object  # noqa: E501
#     'SECURITY_DEFINITIONS': {
#         'basic': {
#             'type': 'basic',
#         },
#     },
#
#     # url to an external Swagger validation service;
#     # defaults to 'http://online.swagger.io/validator/'
#     # set to None to disable the schema validation badge in the UI
#     'VALIDATOR_URL': 'https://online.swagger.io/validator/',
#
#     # swagger-ui configuration settings, see
#     # https://github.com/swagger-api/swagger-ui/blob/112bca906553a937ac67adc2e500bdeed96d067b/docs/usage/configuration.md#parameters
#     'OPERATIONS_SORTER': None,
#     'TAGS_SORTER': None,
#     'DOC_EXPANSION': 'none',
#     'DEEP_LINKING': False,
#     'SHOW_EXTENSIONS': True,
#     'DEFAULT_MODEL_RENDERING': 'model',
#     'DEFAULT_MODEL_DEPTH': 3,
#     'SUPPORTED_SUBMIT_METHODS': ['get', 'put', 'post', 'delete', 'options'],
#     # 'DISPLAY_OPERATION_ID': False,
# }

# REDOC_SETTINGS = {
#     # ReDoc UI configuration settings, see https://github.com/Rebilly/ReDoc#redoc-tag-attributes
#     'LAZY_RENDERING': True,
#     'HIDE_HOSTNAME': False,
#     'EXPAND_RESPONSES': None,
#     'PATH_IN_MIDDLE': False,
# }
