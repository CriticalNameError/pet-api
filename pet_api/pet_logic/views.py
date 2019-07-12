from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status

from core.models import Pets

from pet_logic import serializers

class PetsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    """Manage tags in the database"""
    queryset = Pets.objects.all()
    serializer_class = serializers.PetsSerializer
