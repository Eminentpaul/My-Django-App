from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('topics/', views.topic, name='topic'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('create/room', views.createRoom, name='create-room'),
    path('room/<str:pk>/Room-Environment', views.room, name='room'),
    path('profile/<str:pk>/User-Profile', views.profile, name='profile'),
    path('delete/<str:pk>/Chat/Delete-Chat', views.deleteChat, name='chat-delete'),
    path('deleteHome/<str:pk>/Home-Chat/Delete-Chat', views.deleteChat1, name='chat-delete1'),
    path('delete/<str:pk>/Room/Delete-Room', views.deleteRoom, name='room-delete'),
    path('update/<str:pk>/Room/Update-Room', views.updateRoom, name='update-room'),
    path('edit/<str:pk>/User/Update/User-Profile', views.editProfile, name='edit-user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)