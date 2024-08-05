import socket
import picar_4wd as fc
from picar_4wd.utils import pi_read
import json
from bluedot.btcomm import BluetoothServer

# Moves the car or returns statistics as requested by client for both wifi/bluetooth
def actions(data):
    stats = {}
    if data == b"stop\r\n":
        fc.stop()
    elif data == b"up\r\n":
        fc.forward(100)
    elif data == b"down\r\n":
        fc.backward(100)
    elif data == b"left\r\n":
        fc.turn_left(100)
    elif data == b"right\r\n":
        fc.turn_right(100)
    else:
        pi_stats = pi_read()
        stats['distance'] = fc.us.get_distance()
        stats['temperature'] = str(pi_stats['cpu_temperature']) + '°C'
        stats['battery'] = str(pi_stats['battery']) + "V/8.4V"
    return stats

# --- Bluetooth --- #
# Handles data received, then converts to JSON, encodes and sends back to the client
def received_handler(data):
    bt_socket.send(json.dumps(actions(data)).encode('utf-8'))
bt_socket = BluetoothServer(received_handler, encoding=None) # Creates bluetooth connection

# --- WiFi --- #
HOST = "192.168.1.40" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # removes delay to reuse address
    s.bind((HOST, PORT))
    s.listen()

    try:
        while True:
            client, clientInfo = s.accept()
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            client.sendall(json.dumps(actions(data)).encode('utf-8')) # sends encoded JSON back to client
    except:
        s.close()