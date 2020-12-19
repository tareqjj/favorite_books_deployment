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

        if len(postData['password']) < 8:
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

        if len(postData['password']) < 8:
            errors["pw_length"] = "Password should be at least 8 characters"
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title Name should be at least 1 character"

        if len(postData['description']) < 5:
            errors["description"] = "Description should be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

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

def add_book_DB(book_info, user_id):
    new_book = Book.objects.create(title=book_info['title'], desc=book_info['description'], uploaded_by=User.objects.get(id=user_id))
    Book.objects.get(id=new_book.id).users_who_like.add(User.objects.get(id=user_id))

def add_book_toFavorite(book_id, user_id):
    Book.objects.get(id=book_id).users_who_like.add(User.objects.get(id=user_id))

def remove_book_fromFavorite(book_id, user_id):
    Book.objects.get(id=book_id).users_who_like.remove(User.objects.get(id=user_id))

def editBook(book_id, edited_info):
    Book.objects.filter(id=book_id).update(title=edited_info['title'], desc=edited_info['description'])

def remove_Book(book_id):
    Book.objects.get(id=book_id).delete()

def view_bookInfo(book_id, user_id):
    liked_books = User.objects.get(id=user_id).liked_books.all()
    likedBooks_list=[]
    for book in liked_books:
        likedBooks_list.append(book.id)
    context = {
        'book_info': Book.objects.get(id=book_id),
        'users': Book.objects.get(id=book_id).users_who_like.all(),
        'liked_books': likedBooks_list
    }
    return context

def view_books(user_id):
    liked_books = User.objects.get(id=user_id).liked_books.all()
    likedBooks_list=[]
    for book in liked_books:
        likedBooks_list.append(book.id)

    context = {
        'all_books': Book.objects.all(),
        'liked_books': likedBooks_list
    }
    return context

def view_userPage(user_id):
    context = {
        'all_liked_books': User.objects.get(id=user_id).liked_books.all()
    }
    return context
