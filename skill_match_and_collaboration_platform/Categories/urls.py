from django.urls import path
from .views import AddCatView

urlpatterns = [
    path('addCategories/',AddCatView.as_view(), name= "addCat")
]