from django.urls import path

from . import views


app_name = "room"

urlpatterns = [
    path("", views.home_page, name="home"),


    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_user, name='register'),


    path("room/", views.rooms_page, name="rooms"),
    path("room/<int:room_id>", views.get_room, name="room"),
    path("room/create/", views.createRoom, name="create-room"),
    path("room/edit/<int:room_id>", views.update_room, name="update-room"),
    path('room/delete/<int:room_id>', views.delete_room, name="delete-room"),
    path('room/<int:room_id>/delete-message/<int:msg_id>/', views.delete_message, name='delete-message'),


    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),


    path("profile/<int:user_id>/", views.userProfile, name="profile"),
    path("edit-profile/", views.editUser, name="edit-user"),
]
