import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error + "error")

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send("client1, vid1, client 1 vid1message")
    ws.send("client1, vid2, client 1 vid2message")
    ws.send("client1, vid3, client 1 vid3message")



if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8766",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()