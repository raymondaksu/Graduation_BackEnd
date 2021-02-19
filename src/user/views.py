from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.http import HttpResponseRedirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status, generics
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, ProfileSerializer, UserSerializer, ChangePasswordSerializer, ResetPasswordWithEmailSerializer, SetNewPasswordSerializer
from django.contrib import messages
from .models import Profile

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

# -------------------REGISTER----------------------


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
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

# -------------------USER GET UPDATE DELETE----------------------


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def UserGetUpdateDelete(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Password updated successfully"
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------PROFILE VIEW----------------------


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def ProfileView(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "profile updated successfully"
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------PROFILE LIST VIEW----------------------

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ProfileListView(request):
    profile = Profile.objects.all()

    if request.method == "GET":
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

#--------------------CHANGE PASSWORD VIEW---------------------
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#--------------------RESET PASSWORD VIEW---------------------

class ResetPasswordWithEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordWithEmailSerializer

    def post(self, request):

        email = request.data['email']
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}

            Util.send_email(data)

            return Response({'success':'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Email not registered.'}, status=status.HTTP_404_NOT_FOUND)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error' : 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return HttpResponseRedirect(f'https://fsblog-backend.herokuapp.com/{uidb64}/{token}/', {'uidb64':uidb64, 'token': token})

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error' : 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
