from django.db import models
import bcrypt
import re
# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 1:
            errors["pw_length"] = "Password should be at least 8 characters"

        if postData['password'] != postData['confirm_pw']:
            errors['pw_match'] = "Passwords must match"

        if User.objects.all().filter(email=postData['email']):
            errors['not_unique'] = 'email address already registered'
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 1:
            errors["pw_length"] = "Password should be at least 8 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    user = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="message_comments", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def reg_user(user_info):
    password = user_info['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=user_info['first_name'], last_name=user_info['last_name'], email=user_info['email'], password=hashed)
    user_info = {
        'user_id': new_user.id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
    }
    return user_info

def login_user(user_info):
    user = User.objects.filter(email=user_info['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(user_info['password'].encode(), logged_user.password.encode()):
            user_info = {
                'user_id': logged_user.id,
                'first_name': logged_user.first_name,
                'last_name': logged_user.last_name,
            }
            return user_info
    return False

def add_message(user_id, message_content):
    Message.objects.create(message=message_content['message'], user=User.objects.get(id=user_id))

def add_comment(user_id, comment_info):
    Comment.objects.create(comment=comment_info['comment'], user=User.objects.get(id=user_id), message=Message.objects.get(id=comment_info['message_id']))

def view_wall():
    context = {
        'all_messages': Message.objects.all().order_by('-created_at'),
        'all_comments': Comment.objects.all()
    }
    return context

def remove_message(message_id):
    Message.objects.get(id=message_id).delete()
