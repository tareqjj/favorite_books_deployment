from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('shows', views.shows),
    path('shows/<int:show_id>', views.display_showInfo),
    path('shows/<int:show_id>/edit', views.edit_page),
    path('edit_show/<int:show_id>', views.edit_show),
    path('shows/new', views.add_show_page),
    path('add_show', views.add_show),
    path('shows/<int:show_id>/destroy', views.delete_show),
]
