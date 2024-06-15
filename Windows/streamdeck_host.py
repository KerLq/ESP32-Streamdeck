import socket
from sys import platform, exit
import logging

HEADER = 64
PORT = 5050
SERVER = "192.168.178.24"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

def handle_client(connection, addr):
  print(f"[NEW CONNECTION] {addr} connected.")
  connected = True
  while connected:
    message = connection.recv(HEADER).decode(FORMAT)

    if message:
      print(f"[{addr}] {message}")
      obshandle.send(message)

  connection.close()

def start():
  global obshandle

  if platform in "linux" or platform in "linux2":
    import linux_obshandle as obshandle
  elif platform in "win32":
    import windows_obshandle as obshandle
  else:
    logging.info("You're not on linux or windows!")
    exit()

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(ADDR)
  server.listen()

  print(f"[LISTENTING] Server is listening on {SERVER}")
  while True:
    connection, address = server.accept()
    handle_client(connection, address)