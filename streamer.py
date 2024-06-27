import websocket
import json
import ticker_pb2
import base64
import threading
import time
#RB
#8/4/2024
class Streamer:
    def __init__(self):
        self.data = {}
        self.ws = websocket.WebSocketApp("wss://streamer.finance.yahoo.com",
                                         on_message=self.__on_message,
                                         on_error=self.__on_error,
                                         on_close=self.__on_close)

        self.ws_thread = threading.Thread(target=self.__websocket_run)

    def __decode(self, encoded_data):
        decoded_data = base64.b64decode(encoded_data)
        ticker = ticker_pb2.Ticker.FromString(decoded_data)
        # print("ID:", ticker.id)
        # print("Price:", ticker.price)
        # print("Time:", ticker.time)
        self.data.update({ticker.id:(ticker.price,ticker.time)})

    def __on_message(self, ws, message):
        self.__decode(message)

    def __on_error(self, ws, error):
        print("[-] Error:", error)

    def __on_close(self, ws,*args):
        print("### closed ###")

    def __on_open(self, ws):
        print("[+] WebSocket opened")
        subscribe_message = {"subscribe": [self.subscribe]}
        subscribe_message_str = json.dumps(subscribe_message)
        print("[+] Sent raw:", subscribe_message_str)
        ws.send(subscribe_message_str)

    def __websocket_run(self):
        self.ws.on_open = self.__on_open
        self.ws.run_forever()

    def start_stream(self):
        self.ws_thread.start()

    def stop_stream(self):
        self.ws.close()
        self.ws_thread.join()
        print("Thread stopped")

    def channel(self, subscribe):   
        self.subscribe = subscribe

    def get_data(self):
        temp=self.data.copy()
        self.data.clear()
        return temp





# s = Streamer()
# s.channel("AAPL")
# s.start_stream()

# while(1):
#     time.sleep(2)
#     print(s.get_data())
#     time.sleep(2)
#     # s.stop_stream()

# while(1):
#     data=s.get_data()
#     if data:
#         print(data)

class MultiStreamer:

    def __init__(self):
        self.cthreads=[]
        # self.flag=threading.Event()
        # self.data_lock=threading.Lock()
        self.data={}
        

    def channels(self,subscribe):
        for channel in subscribe:
            ct=Streamer()
            ct.channel(channel)
            self.cthreads.append(ct)

    def start_stream(self):
        for channel in self.cthreads:
            channel.start_stream()

    def get_data(self):
        for channel in self.cthreads:
            temp={}
            while(not temp):
                temp=channel.get_data()
            
            self.data.update(temp)

        # print(self.data)
        temp=self.data.copy()
        self.data.clear()
        return temp

    def stop_stream(self):
        for channel in self.cthreads:
            channel.stop_stream()

# c=MultiStreamer()
# channels=["AAPL","GOOG","MSFT"]

# c.channels(channels)
# c.start_stream()
# for _ in range(10):
#     data=c.get_data()
#     print(data)
        
# c.stop_stream()


