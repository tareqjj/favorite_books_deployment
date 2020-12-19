from django.shortcuts import render, redirect
from django.contrib import messages
from . import models


# Create your views here.
def root(request):
    return redirect('/shows')

def shows(request):
    context = models.display_shows()
    return render(request, 'shows.html', context)

def display_showInfo(request, show_id):
    context = models.show_info(show_id)
    return render(request, 'show_info.html', context)

def edit_page(request, show_id):
    context = {'show_id': show_id}
    return render(request, 'edit_show.html', context)

def edit_show(request, show_id):
    errors = models.Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/' + str(show_id) + '/edit')
    else:
        messages.success(request, "Show successfully updated")
        models.edit_show(show_id, request.POST)
        return redirect('/shows/' + str(show_id))

def add_show_page(request):
    return render(request, 'add_show.html')

def add_show(request):
    errors = models.Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')
    else:
        show_id = models.add_show(request.POST)
        messages.success(request, "Show successfully created")
        return redirect('/shows/' + str(show_id))

def delete_show(request,show_id):
    models.remove_show(show_id)
    return redirect('/shows')

