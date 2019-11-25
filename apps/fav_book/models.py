from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:  
            errors["firstname"] = "User firstname should be at least 2 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "User lastname should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "register password should be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirm'] :
            errors['confirm'] = 'password needs to be match!'
        return errors 

    def login_validator(self,postData):
        errors={}
        # if postData['login_email'] != User.objects.filter(email=postData['login_email']):
        if not User.objects.filter(email=postData['login_email']):
            errors['login_email'] = "Invalid email address!"
        if postData['login_pw'] != User.objects.filter(password=postData['login_pw']) :
            errors['login_pw'] = 'password is in currect!'
        return errors

class BooksManager(models.Manager):
    def Books_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:  
            errors["title"] = "Book title should be at least 2 characters"
        if len(postData['description']) < 3:
            errors["description"] = "Book description should be at least 3 characters"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= UserManager()
    # books_uploaded
    # liked_books
class Books(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    uploaded_by=models.ForeignKey(User,related_name='books_uploaded')
    users_who_like=models.ManyToManyField(User,related_name='liked_books')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= BooksManager()
    