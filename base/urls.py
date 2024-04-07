from django.urls import path
from . import views



urlpatterns = [
    path('',views.home,name = 'home'),
    path('room/<int:pk>/',views.room,name = 'room'),
    path('create-room/',views.room_form,name = 'create_room'),
    path('update-room/<int:pk>/',views.update_room,name = 'update_room'),
    path('delete-room/<int:pk>/',views.delete_room,name = 'delete_room'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerUser, name='register'),
    path('user-profile/<int:pk>/',views.user_profile, name='user_profile'),
    path('delete-comment/<int:pk>/',views.delete_comment,name = 'delete_comment'),
    path('edit-user/',views.edit_user,name = 'edit_user'),
    path('topics/',views.all_topics,name = 'topics'),
    path('activities/',views.all_activity,name = 'activities'),


]