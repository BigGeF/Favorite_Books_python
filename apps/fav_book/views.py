from django.shortcuts import render, HttpResponse,redirect
import bcrypt
from .models import *
from datetime import date, datetime
from django.contrib import messages

def index(request):
    return render(request,"fav_book/index.html")
def show_books(request):
    if 'myuser' in request.session:
        myuser=User.objects.get(id=request.session['myuser'])
        context={
            'firstname':myuser.first_name,
            "allbooks":Books.objects.all(),
            'other_books':Books.objects.exclude(id=request.session['myuser']),
            "user_liked_books":myuser.liked_books.all(),
            # 'uploader':Books.objects.first().uploaded_by,
            
        }
    return render(request,"fav_book/books.html",context)
def show_book_others(request):
    return render(request,"fav_book/books_others.html")

def post_user(request):
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())#密码加密
    errors = User.objects.basic_validator(request.POST)#输入条件限制
    if len(errors) > 0:#输入条件限制
        for key, value in errors.items():#输入条件限制
            messages.error(request, value)#输入条件限制
        return redirect("/")#输入条件限制
    else:
        user = User.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'],email=request.POST['email'],password=hashed_pw)
        request.session['myuser']=user.id
        return redirect('/show_books')

def login(request):
    users=User.objects.filter(email=request.POST['login_email'])
    if len(users)>0:
        if bcrypt.checkpw(request.POST['login_pw'].encode(),users[0].password.encode()):
            request.session['myuser'] = users[0].id
            return redirect("/show_books")
    errors=User.objects.login_validator(request.POST)
    if len(errors) > 0:#输入条件限制
        for key, value in errors.items():#输入条件限制
            messages.error(request, value)#输入条件限制
    return redirect("/")#输入条件限制

def logout(request):
    request.session.clear()
    return render(request,'fav_book/index.html')

def add_book(request):
    errors = Books.objects.Books_validator(request.POST)
    if len(errors) > 0:#输入件限制
        for key, value in errors.items():#输入条件限制
            messages.error(request, value)#输入条件限制
        return redirect("/new_job_page")#输入条件限制
    else:
        Books.objects.create(title=request.POST['title'],description=request.POST['description'],uploaded_by=User.objects.get(id=request.session['myuser'])).users_who_like.add(User.objects.get(id=request.session['myuser']))
        
        #   this_book=Books.objects.create(title=request.POST['title'],description=request.POST['description'],uploaded_by=User.objects.get(id=request.session['myuser']))
        # this_book.save()
        # this_user=User.objects.get(id=request.session['myuser'])
        # this_book.users_who_like.add(this_user)
    return redirect('/show_books')

def add_to_fav(request,id):
    User.objects.get(id=request.session['myuser']).liked_books.add(Books.objects.get(id=id))
    return redirect('/show_books')

def show_books_my(request,id):
    if 'myuser' in request.session:
        context = {
            'firstname':User.objects.get(id=request.session['myuser']).first_name,
            'uploader':Books.objects.first().uploaded_by,
            'title':Books.objects.get(id=id).title,
        }
    return render(request,"fav_book/books_my.html",context)


