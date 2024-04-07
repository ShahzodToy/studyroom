from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm,UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(request):
    q = request.GET.get('q')if request.GET.get('q') != None else ""
    rooms = Room.objects.filter(Q(topic__name__contains = q)|
                                Q(name__contains = q)|
                                Q(description__contains = q))
    topics = Topic.objects.all()[:4]

    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))


    context = {'rooms':rooms,'topics':topics,
               'room_count':room_count,'room_messages':room_messages}

    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participantes = room.participantes.all()
    room.participantes.add(request.user)
    if request.method == 'POST':
        messages = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
            )
        return redirect('room', room.id)

    context = {'room':room,
               'room_messages':room_messages,
               'participantes':participantes}

    return render(request,'base/room.html',context)


def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()


    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/user_profile.html',context)


@login_required(login_url='login')
def room_form(request):
    form_room = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic ,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),

        )
        return redirect('home')
    context = {'form':form_room,'topics':topics}

    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form_room = RoomForm(instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic ,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form_room,'room':room}

    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'base/delete_room.html',context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User is not find')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    context = {}
    return render(request,'register/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Royhat olishda hatolik bor qayta urin')
    return render(request,'register/register.html',{'form':form})

def delete_comment(request,pk):
    message = Message.objects.get(id = pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj':message}
    return render(request,'base/delete_room.html',context)



def edit_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile',pk=user.id)

    return render(request,'base/edit-user.html',{'form':form})

def all_topics(request):
    q = request.GET.get('q')if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(name__icontains = q)
    context = {
        'topics':topics
    }
    return render(request,'base/topics_all.html', context)

def all_activity(request):
    room_message = Message.objects.all()
    return render(request,'base/activity_all.html',{'room_message':room_message})