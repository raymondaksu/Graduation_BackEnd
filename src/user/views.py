from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from django.contrib import messages

@api_view(["POST"])
def RegisterView(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if request.user.is_authenticated:
            messages.warning(request, "You already have an account!")
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "{} created successfully!".format(serializer.validated_data['username'])
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "message": "User could not be created !"
        }
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

