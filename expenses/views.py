from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpenseSerializer
from .models import Expenses
from rest_framework import permissions
from .permissions import IsOwner
# Create your views here.
class ExpenseListAPIView(ListCreateAPIView):
    serializer_class= ExpenseSerializer
    #we need to define  we need to override the method that creates an instance and tell is which owner in this case and set it to current logged in user
    queryset= Expenses.objects.all()
    #defining permission classes just so user who are not authenticate cant access this
    permission_classes=(permissions.IsAuthenticated,)
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    #overriding method get query set as we need to get the objects of the individual user

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    

class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class= ExpenseSerializer
    #we need to define  we need to override the method that creates an instance and tell is which owner in this case and set it to current logged in user
    queryset= Expenses.objects.all()
    #defining permission classes just so user who are not authenticate cant access this, is owner means only the owner can accesss, as we done in permissiosn 
    permission_classes=(permissions.IsAuthenticated, IsOwner,)
    #we create lookup field so that we can access individual query
    lookup_field='id'
    
    
    #overriding method get query set as we need to get the objects of the individual user

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)