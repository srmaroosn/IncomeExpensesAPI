from django.urls import path
from .views import ExpenseDetailAPIView,ExpenseListAPIView
urlpatterns = [
path('list/',ExpenseListAPIView.as_view(), name="list" ),
path('detail/<int:id>/',ExpenseDetailAPIView.as_view(), name="detail" )
]