from django.shortcuts import render, redirect
from django.contrib import messages
from . import models

# Create your views here.
def display_login_reg(request):
    return render(request, 'login_reg_page.html')

def add_user(request):
    errors = models.User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = models.reg_user(request.POST)
        request.session['logged_user_info'] = logged_user
        return redirect('/display_books')

def login(request):
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = models.login_user(request.POST)
        if logged_user:
            request.session['logged_user_info'] = logged_user
            return redirect('/display_books')
        return redirect("/")

def logout(request):
    del request.session['logged_user_info']
    return redirect('/')

def add_book(request):
    errors = models.Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/display_books')
    else:
        models.add_book_DB(request.POST, request.session['logged_user_info']['user_id'])
        return redirect('/display_books')

def add_toFavorite(request, book_id):
    models.add_book_toFavorite(book_id, request.session['logged_user_info']['user_id'])
    return redirect('/books/' + str(book_id))

def remove_fromFavorite(request, book_id):
    models.remove_book_fromFavorite(book_id, request.session['logged_user_info']['user_id'])
    return redirect('/books/' + str(book_id))

def edit_book(request, book_id):
    models.editBook(book_id, request.POST)
    return redirect('/books/' + str(book_id))

def delete_book(request, book_id):
    models.remove_Book(book_id)
    return redirect('/display_books')

def display_bookInfo(request, book_id):
    context = models.view_bookInfo(book_id, request.session['logged_user_info']['user_id'])
    return render(request, 'book_info.html', context)

def display_books(request):
    if 'logged_user_info' in request.session:
        context = models.view_books(request.session['logged_user_info']['user_id'])
        return render(request, 'display_and_add_books.html', context)
    else:
        return redirect("/")

def display_userPage(request):
    context = models.view_userPage(request.session['logged_user_info']['user_id'])
    return render(request, 'user_page.html', context)
