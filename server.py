#!/usr/bin/env python

# WS server example

import asyncio
import websockets
from collections import defaultdict

users = {}
videos = defaultdict(list)


async def receive(websocket, path):
    # Check if client disconnected remove associated record entries
    try:
        message = await websocket.recv()
    except:
        for n in users:
            if users[n] == websocket:
                videostoremove = list()
                for o in videos:
                    if n in videos[o]:
                        videos[o].remove(n)
                    if len((videos[o])) == 0:
                        videostoremove += {o}

                for o in videostoremove:
                    videos.pop(o)
                users.pop(n)
                break
        return

    message = message.split(', ', 2)
    print("recieved message: ", message)
    if len(message) == 1:
        print("to few arguments")
        return
    if len(message) == 2:
        if 'tempUID' not in receive.__dict__:
            receive.tempUID = 0
        uid = receive.tempUID
        receive.tempUID += 1
        vid = message[0]
        sendmessage = message[1]
    else:
        uid = message[0]
        vid = message[1]
        sendmessage = uid + " " + message[2]

    users[uid] = websocket
    if uid not in videos[vid]:
        videos[vid].append(uid)

    for n in videos[vid]:
        print (n)
        await users[n].send(sendmessage)

    await receive(websocket, path)

start_server = websockets.serve(receive, "localhost", 8766)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()