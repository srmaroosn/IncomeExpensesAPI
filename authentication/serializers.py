from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# smart_str, force, smart enable us that we are sending the conventional data
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=60, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should contain alphanumeric character")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerficationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200, min_length=1)
    password = serializers.CharField(
        max_length=60, min_length=8, write_only=True)
    # we put read only true so that these fields wont be mandetory while logging in
    username = serializers.CharField(
        max_length=60, min_length=8, read_only=True)
    tokens = serializers.CharField(
        max_length=100, min_length=2, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        # checking for user activities

        if not user:
            raise AuthenticationFailed('Invalid Credentials, Try again!')

        if not user.is_active:
            raise AuthenticationFailed("Account Disabel, COntact Admin")

        if not user.is_verified:
            raise AuthenticationFailed("Email not verified, COntact Admin")

        # returning the details of the user
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200, min_length=1)

    class Meta:
        
        fields = ['email']

    # validating the data


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)
    token = serializers.CharField( min_length=1, write_only=True)
    uidb64 = serializers.CharField( min_length=1, write_only=True)

    class Meta:
        fields=['password','token','uidb64']

    #validation

    def validate(self, attrs):
        try:
            #gettting the attributes
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            
            #decoding
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                
                raise AuthenticationFailed("The reset link is invalid, Already used token", 401)
            #setting new password
            user.set_password(password)
            user.save()


            return (user)
        except Exception as e:
            
            raise AuthenticationFailed("The reset link is invalid", 401)

        return super().validate(attrs)
    
                
      
    
