from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
#buiding our custom models

class UserManager(BaseUserManager):

    #we overriding the create user method
    def create_user(self, username,email,password=None):
        if username is None:
            raise TypeError('User should have a valid username')
        if email is None:
            raise TypeError('User should have a valid Email')
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user



    #creating super user
    def create_superuser(self, username,email,password=None):
        if username is None:
            raise TypeError('User should have a valid username')
        if password is None:
            raise TypeError('User should not be none')
        if email is None:
            raise TypeError('User should have a valid Email')
        
    
        user=self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    

#creating the user model

class User(AbstractBaseUser, PermissionsMixin):
    username= models.CharField(max_length=225, unique=True,db_index=True )
    email= models.EmailField(max_length=225, unique=True,db_index=True )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)  
    created_at = models.TimeField(auto_now_add=True) #auto_now_add gives starting time
    updated_at = models.TimeField(auto_now=True)  #auto now gives updated time

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #tell django how to manege of this user 
    objects=UserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        #token for the current user that is denoted by the self

        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }