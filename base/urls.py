from django.urls import path
from . import views



urlpatterns = [
    path("",views.home,name='home'),
    
    path("login",views.loginFunc,name='Login'),
    path("logout",views.logoutFunc,name="Logout"),
    path("register",views.register,name='register'),
    path("userProfile/<str:id>",views.userProfile,name="user-profile"),

    path("room/<str:pk>",views.room,name='room'),
    path("createRoom",views.createRoom,name='create-room'),
    path("updateRoom/<int:pk>",views.updateRoom,name='update-room'),
    path("deleteRoom/<str:id>",views.deleteRoom,name='delete-room'),
    path("deleteMessage/<str:id>",views.deleteMessage,name='delete-message'),
]
