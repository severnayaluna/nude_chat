# __import__('builtins').__dict__['getattr']

# getattr(__import__('sys').__dict__.__getitem__('stdout'), 'write')(getattr(__import__('builtins').__dict__.__getitem__('str'), 'join')('', __import__('builtins').__dict__.__getitem__('list')((getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xbf', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x80', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb8', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb2', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb5', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x82', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b' ', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xbc', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb8', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x80', 'utf-8'), '\n'))))


# string = r"""
# getattr(__import__('sys').__dict__.__getitem__('stdout'), 'write')(getattr(__import__('builtins').__dict__.__getitem__('str'), 'join')('', __import__('builtins').__dict__.__getitem__('list')((getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xbf', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x80', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb8', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb2', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb5', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x82', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b' ', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xbc', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb8', 'utf-8'), getattr(__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x80', 'utf-8'), '\n'))))
# """

# print(string.replace('getattr', r"""__import__('builtins').__dict__['getattr']"""))

# __import__('builtins').__dict__['getattr'](__import__('sys').__dict__.__getitem__('stdout'), 'write')(__import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('str'), 'join')('', __import__('builtins').__dict__.__getitem__('list')((__import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xbf', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x80', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb8', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb2', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb5', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x82', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b' ', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xbc', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd0\xb8', 'utf-8'), __import__('builtins').__dict__['getattr'](__import__('builtins').__dict__.__getitem__('bytes'), 'decode')(b'\xd1\x80', 'utf-8'), '\n'))))

# def gen():
#     a = 0
#     while a < 5:
#         a += 1
#         yield a**2

# i = gen()
# b = [next(i) for _ in range(10)]
# print(b)

# users = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# [print(f'{idx+1}: {users[:idx] + users[idx+1:]}') for idx, value in enumerate(users)]

import asyncio

import json

from redis.asyncio import Redis

from bot.my_queue.my_queue import Queue, Room


async def main() -> None:
    storage = Redis(host='localhost', port=6379, decode_responses=True)
    await storage.flushall()

    queue = Queue(storage)
    room = Room(storage)

    [
        await queue.add_user(i) for i in range(10000, 10100)
    ]

    users = await room.try_create_room(queue, 2)

    print(f'Users: {users}')
    [
        print(f'{id_}: ', (await storage.get(f"from_{id_}")))
        for id_ in users
    ]

    await storage.aclose()
    # a = [*range(10)]
    # print(a, bytes(a))


asyncio.run(main())
