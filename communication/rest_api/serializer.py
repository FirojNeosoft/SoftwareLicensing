from rest_framework import serializers

from communication.models import *


class SMSSerializer(serializers.ModelSerializer):
    """
    SMS Serializer
    """

    class Meta:
        model = SMS
        fields = ('id', 'mobile', 'message', 'status', 'created_at')
        read_only_fields = ('id', 'created_at',)
