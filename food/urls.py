from django.urls import path
from . import views

app_name = "food"

urlpatterns = [
    path('randreci/', views.randreci, name="randreci"),
    path('recoreci/', views.recoreci, name="recoreci"),
    path('test/', views.test, name="test"),
]
