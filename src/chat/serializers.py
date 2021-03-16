# from django.contrib.auth import get_user_model
# User = get_user_model()
# from rest_framework import serializers


# class MessageGetSerializer(serializers.ModelSerializer):
#     sender = serializers.StringRelatedField()
#     receiver = serializers.StringRelatedField()

#     class Meta:
#         model = Message
#         fields = ['sender', 'receiver', 'message', 'timestamp']

# class MessagePostSerializer(serializers.ModelSerializer):
#     sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
#     receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

#     class Meta:
#         model = Message
#         fields = ['sender', 'receiver', 'message', 'timestamp']
