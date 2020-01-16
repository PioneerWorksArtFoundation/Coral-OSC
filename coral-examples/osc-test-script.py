from oscpy.client import OSCClient
from time import sleep

osc = OSCClient('192.168.100.89', 8080)
while(True):
    messageText = "hello".encode("utf8")
    osc.send_message(b'/ping', messageText)
    print("Sent message!\n\n")
    sleep(1)
