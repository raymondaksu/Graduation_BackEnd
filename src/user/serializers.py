from django.http import request
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile
from dj_rest_auth.serializers import TokenSerializer

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, force_bytes, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class RegistrationSerializer(serializers.ModelSerializer):
    # Overwriting fields
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[
                                     validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'})

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2"
        )

    def validate(self, attrs):  # attrs is not a special expression
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password didn't match"}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "image",
            "bio",
        )


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[
                                     validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
            "username": {"read_only": True},
            "email": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password didnt match"}
            )
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

# ------------------Token Serializer---------------------

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProfileTokenSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('image',)

    def get_image(self, obj):
        request = self.context['request']
        profile = Profile.objects.get(user=request.user)
        return print(profile.image)


class CustomTokenSerializer(TokenSerializer):
    user = UserTokenSerializer(read_only=True)
    profile_image = ProfileTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user', 'profile_image')

# ----------------Change Password-----------------------------

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# ----------------Reset Password------------------------------


class ResetPasswordWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password', 'token', 'uidb64']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)