from bot.queue.queue import Queue, Room


for i in range(999):
    Queue.add_user(i)


print(Room.try_create_room())
print(Room.try_create_room())
print(Room.redirect_from(851))
