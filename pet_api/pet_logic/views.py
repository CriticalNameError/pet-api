from rest_framework import viewsets, mixins

from core.models import Pets

from pet_logic import serializers


class PetsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    """Manage pets in the database"""
    queryset = Pets.objects.all()
    serializer_class = serializers.PetsSerializer
