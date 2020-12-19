from django.urls import path     
from . import views


urlpatterns = [
    path('', views.display_login_reg),
    path('add_user', views.add_user),
    path('login', views.login),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('display_books', views.display_books),
    path('add_toFavorite/<int:book_id>', views.add_toFavorite),
    path('remove_fromFavorite/<int:book_id>', views.remove_fromFavorite),
    path('books/<int:book_id>/edit', views.edit_book),
    path('books/<int:book_id>', views.display_bookInfo),
    path('books/<int:book_id>/destroy', views.delete_book),
    path('books/user', views.display_userPage)
]

