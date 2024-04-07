from django.contrib import admin
from .models import Room, Topic, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['host','name','topic']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room','body']

admin.site.register(Topic)