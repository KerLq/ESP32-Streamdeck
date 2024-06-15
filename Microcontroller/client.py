import usocket as socket
from time import sleep
import network

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "Lokale IP-Adresse"
ADDR = (SERVER, PORT)

def initialize():
  timeout = 0 # WiFi Connection Timeout variable 

  wifi = network.WLAN(network.STA_IF)
  
  wifi.active(False)
  sleep(0.5)
  wifi.active(True)

  wifi.connect("SSID", "Passwort")
  
  if not wifi.isconnected():
      print('connecting..')
      while (not wifi.isconnected() and timeout < 5):
          print(5 - timeout)
          timeout = timeout + 1
          sleep(1)
          
  print("Connected")

  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(ADDR)

  return client

def send(self, message):
  message = message.encode('utf-8')
  client.send(message)
    
