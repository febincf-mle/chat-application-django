from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from authentication.forms import UserForm
from .models import Room, Topic, Message


User = get_user_model()

def rooms_page(request):

    # Query all the available rooms
    available_rooms = Room.objects.all()

    return render(request, "room/rooms.html", {
        "rooms": available_rooms
    })


def get_room(request, room_id):

    room = Room.objects.get(pk=room_id)
    # Get all the room messages
    messages = room.room_messages.all().order_by("-updated_at")
    participants = room.participants.all()
    total_participants = participants.count()


    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("comment")
        )
        room.participants.add(request.user)
        return redirect("room:room", room.id)

    return render(request, 'room/room.html', {
        "room": room,
        "messages": messages,
        "participants": participants,
        "total_participants": total_participants,
    })


@login_required(login_url="/login")
def userProfile(request, user_id):

    user = User.objects.get(pk=user_id)
    rooms = user.created_rooms.all() # Rooms hosted by the selected user
    topics = Topic.objects.all()
    user_messages = user.user_messages.all()


    return render(request, 'room/profile.html', {
        "user": user,
        "rooms": rooms,
        "room_messages": user_messages,
        "topics": topics,
    })


@login_required(login_url='/login')
def createRoom(request):

    if request.method == 'POST':

        name = request.POST.get("name")
        description = request.POST.get("description")
        topic_name = request.POST.get("topic")

        host = request.user
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(name=name, description=description, host=host, topic=topic)

        return redirect("room:home")


    topics = Topic.objects.all()
    users = User.objects.all()

    return render(request, 'room/create-room.html', {
        "topics": topics,
        "users": users,
    })


@login_required(login_url='room:login')
def update_room(request, room_id):

    selected_room = Room.objects.get(pk=room_id)

    if request.method == 'POST':

        selected_room.name = request.POST.get("name")
        selected_room.description = request.POST.get("description")
        topic_name = request.POST.get("topic")

        topic, created = Topic.objects.get_or_create(name=topic_name)
        selected_room.topic = topic

        selected_room.save()
        return redirect("room:home")


    topics = Topic.objects.all()
    users = User.objects.all()

    return render(request, 'room/update-room.html', {
        "topics": topics,
        "users": users,
        "room": selected_room,
    })


@login_required(login_url='/login')
def delete_room(request, room_id):

    selected_room = Room.objects.get(pk=room_id)

    if request.method == 'POST':
        selected_room.delete()
        return redirect("room:home")

    return render(request, 'room/delete.html', {
        "name": selected_room.name,
    })


@login_required(login_url='/login')
def delete_message(request, room_id, msg_id):

    message = Message.objects.get(pk=msg_id)

    if request.method == 'POST':
        message.delete()
        return redirect("room:room", room_id)

    return render(request, 'room/delete.html', {
        "name": " this message"
    })


def topicsPage(request):

    q = request.GET.get("q") if request.GET.get("q") else ""
    topics = Topic.objects.filter(name__icontains=q)

    room_count = Room.objects.all().count()

    return render(request, 'room/topics.html', {
        "topics": topics,
        "room_count": room_count,
    })


@login_required(login_url="/login")
def editUser(request):
    user = request.user
    form = UserForm(instance=user)


    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("room:profile", user.id)

    return render(request, 'room/edit-user.html', {
        "user": user,
        "form": form,
    })


def activityPage(request):

    room_messages = Message.objects.all()
    return render(request, 'room/activity.html', {
        "room_messages": room_messages,
    })