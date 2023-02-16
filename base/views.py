from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages as mg
from .form import RoomForm, RegForm, UpdateUserProfie
from .models import Room, Topic, Message, User
from django.db.models import Q

# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else: mg.info(request, 'Invalid Username or Password')

    return render(request, 'login.html')


def register(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('home')
        else: mg.info(request, 'Registration not Successful')
    return render(request, 'signup.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[:3]
    messages = Message.objects.all()

    context = {'rooms':rooms, 'topics':topics, 'messages':messages}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')


    context = {'form':form, 'topics':topics}
    return render(request, 'create-room.html', context)

def topic(request):
    topics = Topic.objects.all()
    return  render(request, 'topics.html', {'topics': topics})

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topic = room.topic.name
    form = RoomForm(instance=room)
    update = True

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topics, create = Topic.objects.get_or_create(name=topic_name)
        room.topic = topics
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')

        if True:
            room.save()
            return redirect('room', pk=room.id)
        else: mg.info(request, 'Room Not Updated ')

    return render(request, 'create-room.html.', {'form':form, 'topic':topic, 'update': update})

def deleteChat(request, pk):
    obj = Message.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('room', pk=obj.roomName.id)
    return render(request, 'delete.html', {'obj': obj})

def deleteChat1(request, pk):
    obj = Message.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': obj})

def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': obj})

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user = request.user,
            roomName = room,
            body = request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'messages': messages, 'participants': participants}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    messages = user.message_set.all()

    context = {'user': user, 'rooms': rooms, 'topics': topics, 'messages': messages}
    return render(request, 'profile.html', context)

def editProfile(request, pk):
    user = User.objects.get(id=pk)
    form = UpdateUserProfie(instance=user)

    if request.method == 'POST':
        update = UpdateUserProfie(request.POST, request.FILES, instance=user)
        if update.is_valid():
            update.save()
            return redirect('profile', pk=user.id)
    return render(request, 'edit-user.html', {'form':form})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('home')