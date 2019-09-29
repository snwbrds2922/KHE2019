#!/usr/bin/env python

# WS server example

import asyncio
import websockets
from collections import defaultdict
import random, signal, sys

users = {}
videos = defaultdict(list)

file = open('server.log', 'a+')

def signal_handler(sig, frame):
    print("exiting")
    file.close()
    sys.exit(0)

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
                            await users[p].send("UPDATE:" + str(len(videos[o])))
                    if len((videos[o])) == 0:
                        videostoremove += {o}

                for o in videostoremove:
                    videos.pop(o)
                print(str(n) + " left")
                users.pop(n)
                break
        return

    print("received message: " + message +'\n')
    file.write("received message: " + message +'\n')
    if len(message) < 2:
        file.write("received empty message\n")
        await websocket.send("EMPTY RECEIVED")
        return

    message = message.split(':', 3)
    if message[0] == "CONNECT":
        if len(message) < 2:
            print("NOVID")
            await websocket.send("NO VIDID RECEIVED")
            file.write("RECEIVED CONNECT NO VID\n")
            print("RECEIVED CONNECT NO VID\n")
            return

        uid = random.randint(1, 1000)
        while uid in users:
            uid = random.random(1, 1000)
        users[uid] = websocket
        vid = message[1]
        for n in users:
            if n == websocket:
                searchuid = n
                for o in videos:
                    for p in videos[o]:
                        if p == searchuid:
                            videos[o].pop(p)
                            print("removed ", searchid)
                            break
                    if len((videos[o])) == 0:
                        videos.pop(o)
                        break
        
        if uid not in videos[vid]:
            videos[vid].append(uid)
        for n in videos[vid]:
            await users[n].send("UPDATE:" + str(len(videos[vid])))

    elif message[0] == "MESSAGE":
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
    else:
        file.write("invalid header\n")
        print("invalid header\n")
        await websocket.send("INVALID HEADER")

    await receive(websocket, path)

# For Server
start_server = websockets.serve(receive, "157.245.135.82", 8766)
#For local
#start_server = websockets.serve(receive, "localhost", 8766)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
