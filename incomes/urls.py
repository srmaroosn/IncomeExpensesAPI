from django.urls import path
from .views import IncomeDetailAPIView,IncomeListAPIView
urlpatterns = [
path('list/',IncomeListAPIView.as_view(), name="list" ),
path('detail/<int:id>/',IncomeDetailAPIView.as_view(), name="detail" )
]