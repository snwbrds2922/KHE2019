#!/usr/bin/env python

# WS server example

import asyncio
import websockets
from collections import defaultdict
import random

users = {}
videos = defaultdict(list)

file = open("server.log", "a")

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
                        for p in videos[o]:
                            await users[p].send("UPDATE:" + str(len(videos)))
                    if len((videos[o])) == 0:
                        videostoremove += {o}

                for o in videostoremove:
                    videos.pop(o)
                users.pop(n)
                break
        return

    message = message.split(':', 3)
    print("received message: ", message)
    if len(message) == 0:
        file.write("received empty message\n")
        await websocket.send("EMPTY RECEIVED")
        return
    
    if message[0] == "CONNECT":
        if len(message) < 2:
            print("NOVID")
            await websocket.send("NO VIDID RECEIVED")
            return

        uid = random.randint(1,1000)
        while uid in users:
            uid = random.random(1,1000)
        users[uid] = websocket
        vid = message[1]
        if uid not in videos[vid]:
            videos[vid].append(uid)
        for n in videos[vid]:
            await users[n].send("UPDATE:" + str(len(users)))

    if message[0] == "MESSAGE":
        if len(message) < 2:
            await websocket.send("NOMSGDATA")
        else:
            for n in users:
                if users[n] == websocket:
                    uid = n
            for n in videos:
                if uid in videos[n]:
                    for o in videos[n]:
                        await users[o].send(str("MESSAGE:" + str(uid) + ':' + message[1]))

    await receive(websocket, path)

"""  
    if len(message) == 2:

        uid = receive.tempUID
        receive.tempUID += 1
        vid = message[0]
        sendmessage = message[1]
    else:
        uid = message[0]
        vid = message[1]
        sendmessage = uid + ", " + message[2]

    users[uid] = websocket


    for n in videos[vid]:
        print (n)
        await users[n].send(sendmessage)
"""


start_server = websockets.serve(receive, "localhost", 8766)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()