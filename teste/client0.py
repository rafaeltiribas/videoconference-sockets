from vidstream import CameraClient
from vidstream import StreamingServer
from vidstream import AudioSender
from vidstream import AudioReceiver

import threading
import time
import socket

receiving = StreamingServer('192.168.0.177', 7777)
sending = CameraClient('192.168.0.177', 8888)

t1 = threading.Thread(target=receiving.start_server)
t1.start()

time.sleep(5)

t2 = threading.Thread(target=sending.start_stream)
t2.start()

receiver = AudioReceiver('192.168.0.177', 7776)
sender = AudioSender('192.168.0.177', 8887)

receiver_thread = threading.Thread(target=receiver.start_server)
receiver_thread.start()

time.sleep(5)

sender_thread = threading.Thread(target=sender.start_stream)
sender_thread.start()

while input("") != "STOP":
    continue

receiving.stop_server()
sending.stop_stream()