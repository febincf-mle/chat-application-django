from django.shortcuts import render
from django.db.models import Q
from room.models import Room, Topic, Message

def home_page(request):

    q = request.GET.get("q") if request.GET.get("q") else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(room__topic__name__icontains=q)
    )

    room_count = rooms.count()

    return render(request, 'room/home.html', {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    })