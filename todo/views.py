from django.shortcuts import render, redirect, get_object_or_404      
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 调用Django自身的框架，创建用户注册机能。
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required        #确保只有登陆的用户才能在网页中进行修改


def home(request):
    return render(request, 'todo/home.html')

# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})  # 指向template/signupuers.html
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])         # Create a new user
                user.save()
                login(request, user)
                return redirect('currenttodos')     #***(调用redirect.) 先让用户注册，然后保存用户，之后登陆用户，将页面转移到currenttodos.html

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new user'})

        else:
        # Tell the user the passwords didn't match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})  # 指向template/loginusers.html
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':                 #对数据库进行修改时，用POST
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:                                     #这里的try-except函数，是为了防止题目中输入的内容超过规定。如果超过限制，则返回重新输入,并显示提示语句error。
            form = TodoForm(request.POST)        #将创建的TodoForm里的内容赋值给form
            newtodo = form.save(commit=False)    #将上面的form赋值给newtodo，但是不保存到数据库
            newtodo.user = request.user          #新创建的todo的user必须同数据库中为同一个user，保证了创立事件归属同一主人。
            newtodo.save()                       #保存新的newtodo
            return redirect('currenttodos')      #跳转到currenttodo页面
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)     #根据限定条件，找到对应于目标用户的todo，进行输出。
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')     #按照完成时间的倒序进行排列
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):                  #进到具体的todolist内容里面。
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':                  #请求为查找资源，且无副作用（不修改数据库）时候，用GET
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request, todo_pk):               #完成任务，删除对应的项目，显示剩余项目
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':                  #对数据库进行修改时，用POST
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):               #完成任务，删除对应的项目(和上面的不同是，这一次从数据库中删除了数据)
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':                  #对数据库进行修改时，用POST
        todo.delete()
        return redirect('currenttodos')