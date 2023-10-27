import socket
import time
import json
import urllib.parse
from datetime import datetime
from http.server import HTTPServer
from pathlib import Path
from threading import Thread
from server import Server


HOST_NAME = 'localhost'
PORT_NUMBER = 3000
SOCKET_IP = 'localhost'
SOCKET_PORT = 5000
STORAGE_DIR = Path().joinpath('storage')
FILE_STORAGE = STORAGE_DIR / 'data.json'


def run_http_server():
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        

def run_socket_server(ip=SOCKET_IP, port=SOCKET_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    
    try:
        while True:
            data, address = sock.recvfrom(1024)
            save_data_to_json(data)
    except KeyboardInterrupt:
        sock.close()
        
def save_data_to_json(data):
    data_parse = urllib.parse.unquote_plus(data.decode())
    data_dict = {key: value for key, value in [
        el.split('=') for el in data_parse.split('&')]}

    try:
        with open(FILE_STORAGE, 'r') as f:
            storage = json.load(f)
    except ValueError:
        storage = {}

    storage.update({str(datetime.now()): data_dict})

    with open(FILE_STORAGE, 'w') as f:
        json.dump(storage, f)


if __name__ == '__main__':
    STORAGE_DIR.mkdir(exist_ok=True)
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w') as f:
            json.dump({}, f)
            
    try:
        print(time.asctime(), f'Server UP - {HOST_NAME} {PORT_NUMBER}')
        
        http_server = Thread(target=run_http_server)
        socket_sever = Thread(target=run_socket_server)
        http_server.daemon = True
        http_server.start()
        socket_sever.daemon = True
        socket_sever.start()
    
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print(time.asctime(), f'Server DOWN - {HOST_NAME} {PORT_NUMBER}')
        exit()
    
    # httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    # print(time.asctime(), f'Server UP - {HOST_NAME} {PORT_NUMBER}')
    
    # try:
    #     httpd.serve_forever()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     httpd.server_close()
    
    
    print(time.asctime(), f'Server DOWN - {HOST_NAME} {PORT_NUMBER}')
    

