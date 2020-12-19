from django.db import models
from django.utils import timezone

# Create your models here.
class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['title']) < 2:
            errors["title"] = "Show title should be at least 2 characters"
        if len(postData['network']) < 3:
            errors["network"] = "Show network should be at least 3 characters"
        if postData['desc'] != "":
            if len(postData['desc']) < 10:
                errors["desc"] = "Show description should be at least 10 characters"
        if postData['release_date'] > str(timezone.now()):
            errors['release_date'] = "Show release date should be in the past"
        if Show.objects.all().filter(title=postData['title']):
            errors['not_unique'] = 'Show title should be unique'
        return errors

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    desc = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

def display_shows():
    context = {'all_shows': Show.objects.all()}
    return context

def show_info(show_id):
    context = {'show_info': Show.objects.get(id=show_id)}
    return context


def edit_show(show_id, updated_info):
    Show.objects.filter(id=show_id).update(title=updated_info['title'], network=updated_info['network'],
                        release_date=updated_info['release_date'], desc=updated_info['desc'])

def add_show(show_info):
    new_show = Show.objects.create(title=show_info['title'], network=show_info['network'],
                        release_date=show_info['release_date'], desc=show_info['desc'])
    return new_show.id

def remove_show(show_id):
    Show.objects.get(id=show_id).delete()
