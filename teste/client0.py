from vidstream import CameraClient
from vidstream import StreamingServer

import threading
import time
import socket

receiving = StreamingServer(socket.gethostbyname(socket.gethostname()), 7777)
sending = CameraClient(socket.gethostbyname(socket.gethostname()), 8888)

t1 = threading.Thread(target=receiving.start_server)
t1.start()

time.sleep(2)

t2 = threading.Thread(target=sending.start_stream)
t2.start()

while(input("")) != "STOP":
    continue

receiving.start_server()
sending.stop_stream()