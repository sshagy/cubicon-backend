from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'contest', views.ContestViewSet)
router.register(r'round', views.RoundViewSet)
router.register(r'result', views.ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]