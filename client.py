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
    #ws.send("")
    ws.send("CONNECT:VID1234")
    ws.send("MESSAGE:hello world!")
    ws.send("MESdfSAGE")


if __name__ == "__main__":
    #websocket.enableTrace(True)
    # For SERVER
    #ws = websocket.WebSocketApp("ws://157.245.135.82:8766",
    # For local
    ws = websocket.WebSocketApp("ws://localhost:8766",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()