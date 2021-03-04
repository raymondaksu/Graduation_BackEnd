from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models.query_utils import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageGetSerializer, MessagePostSerializer
from user.models import User

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        sender = get_object_or_404(User, username=sender)
        receiver = get_object_or_404(User, username=receiver)
        messages = Message.objects.filter(Q(sender_id=sender, receiver_id=receiver) | Q(sender_id=receiver, receiver_id=sender))
        serializer = MessageGetSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessagePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)