from rest_framework import generics
from .serializers import RegisterSerializers, EmailVerficationSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer

from rest_framework.response import Response
from rest_framework import status, views
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
# reverse use the name of the urls and give us the path
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# smart_str, force, smart enable us that we are sending the conventional data
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializers
    renderer_classes= (UserRenderer,)
    def post(self, request):
        user = request.data
        serializers = self.serializer_class(data=user)
        # this runs validate from serializers
        serializers.is_valid(raise_exception=True)
        # this runs create method from the serializers
        serializers.save()
        # after creating it return the data of the user from serializer
        user_data = serializers.data
        user = User.objects.get(email=user_data['email'])
        # get token for specific user
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('verify-email')
        # we get the link without protocol now we define the protocol i.e link
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # construct message
        email_body = 'Hi\n' + user.username + '\n' + \
            'Use the link below to verify your email. \n'+absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'verify your email'}
        # as this is static we dont have to use like util=util.send_email
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    
    serializer_class = EmailVerficationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    renderer_classes= (UserRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class=ResetPasswordEmailRequestSerializer
    def post(self, request):
        #pick data which user gives and send to serializer for validation 
        
        serializer=self.serializer_class(data=request.data)
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
                # sending email to respective user containing token
                # encoding the user id
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                # creating token
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                #passing the uid64 and token as kwargs ditionery
                relativeLink = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})

                absurl = 'http://'+current_site +  relativeLink

                email_body = 'Hello\n'  + '\n' + \
                    'Use the link below to Reset your password. \n'+absurl
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset your password'}

                Util.send_email(data)
        #telling user we send a email of reset passwprd
        return Response({"sucess":'We have send you a password reset email'}, status=status.HTTP_200_OK)

#handling get rrequest when user click on link it should validate by get request
class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            #smart str utility to create in string, decoding the user as send on the link
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            #check id if  user use it for the second time
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({"Error":'Token is not valid. Enter a valid token'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'sucess':True,'message':'Credential valid', 'uidb64':uidb64, 'Token':token}, status= status.HTTP_200_OK)

            
        except DjangoUnicodeDecodeError as identifier:
            return Response({"Error":'Token is not valid. Enter a valid token'}, status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
