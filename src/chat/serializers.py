from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message


class MessageGetSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

class MessagePostSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
