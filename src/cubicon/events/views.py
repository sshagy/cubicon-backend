from rest_framework import viewsets
from rest_framework import permissions
from . import models, serializers as srlz


class ContestViewSet(viewsets.ModelViewSet):
    queryset = models.Contest.objects.all().order_by('-start_date')
    serializer_class = srlz.ContestSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoundViewSet(viewsets.ModelViewSet):
    queryset = models.Round.objects.all()
    serializer_class = srlz.RoundSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all().order_by('pos')
    serializer_class = srlz.ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
