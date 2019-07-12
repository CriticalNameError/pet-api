from rest_framework import serializers

from core.models import Pets


class PetsSerializer(serializers.ModelSerializer):
    """Serializer for pets object instances"""

    class Meta:
        model = Pets
        fields = ('id', 'name', 'species', 'gender', 'birthday')
        read_only_fields = ('id', )
