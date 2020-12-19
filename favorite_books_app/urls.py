from django.urls import path     
from . import views


urlpatterns = [
    path('', views.display_login_reg),
    path('add_user', views.add_user),
    path('login', views.login),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('wall', views.display_wall),
    path('post_comment', views.post_comment),
    path('delete/<int:user_id>/<int:message_id>', views.delete_message),
]

