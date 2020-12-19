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
        return redirect('/wall')

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
            return redirect('/wall')
        return redirect("/")

def logout(request):
    del request.session['logged_user_info']
    return redirect('/')

def post_message(request):
    models.add_message(request.session['logged_user_info']['user_id'], request.POST)
    return redirect('/wall')

def post_comment(request):
    models.add_comment(request.session['logged_user_info']['user_id'], request.POST)
    return redirect('/wall')


def display_wall(request):
    if 'logged_user_info' in request.session:
        context = models.view_wall()
        return render(request, 'wall_main.html', context)
    else:
        return redirect("/")

def delete_message(request, user_id, message_id):
    if user_id == request.session['logged_user_info']['user_id']:
        models.remove_message(message_id)
    return redirect('/wall')

