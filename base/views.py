from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room,Topic,Message
from .forms import RoomForm


# Create your views here.



def loginFunc(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"user does not exit")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password is incorrect')
    context ={'page':page}
    return render(request,'base/login_register.html',context)


def logoutFunc(request):
    logout(request)
    return redirect('home')

def register(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
    context = {'page':page,'form':form}
    return render(request,"base/login_register.html",context)


def home(request):
    q = request.GET.get('q') if request.GET.get("q") != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms,'topics':topics,'room_count':room_count,"room_meesages":room_messages}
    return render(request,"base/home.html",context)


@login_required(login_url="Login")
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room",pk=room.id)
    context = {"room":room,'room_messages':room_messages,"participants":participants}
    return render(request,"base/room.html",context)



@login_required(login_url="Login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {'form':form}
    return render(request,"base/room_form.html",context)

@login_required(login_url="Login")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("you are not the user to this room")
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {'form':form}
    return render(request,"base/room_form.html",context)


@login_required(login_url="Login")
def deleteRoom(request,id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return HttpResponse("you cant delete this room")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj":room}
    return render(request,"base/delete.html",context)


@login_required(login_url='Login')
def userProfile(request,id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messag':room_messages,'topics':topics}
    return render(request,"base/profile.html",context)



@login_required(login_url="Login")
def deleteMessage(request,id):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse("you cant delete this room")
    if request.method == "POST":
        message.delete()
        return redirect("home")
    context = {"obj":message}
    return render(request,"base/delete.html",context)




