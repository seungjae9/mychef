from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>/', views.detail, name="detail"),
    path('create/', views.create, name="create"),
    path('hashtags/<int:id>/', views.hashtags, name="hashtags"),
    path('<int:id>/like/', views.like, name="like"),
    path('<int:id>/update/', views.update, name="update"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/comment/create/', views.comment_create, name="comment_create"),
    path('<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name="comment_delete"),
    path('search/', views.search, name="search"),
]
