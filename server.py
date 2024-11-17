import random
import numpy as np
from min_hero_classes import Minion, BaseMinion, Gem
import os
import socket
import threading
import ast

if not os.path.exists("active_minions"):
    os.makedirs("active_minions")

if not os.path.exists("minions"):
    os.makedirs("minions")


#load the content of every file inside the minions folder in a list, the list is order by file last modification
def load_minions():
    file_list = os.listdir("active_minions")
    file_list.sort(key=lambda x: os.path.getmtime(f"active_minions/{x}"))
    minions = []
    for file in file_list:
        with open(f"active_minions/{file}", 'r', encoding="utf-8") as f:
            minion_data = f.read()
            minions.append(minion_data)
    return minions


class GameSocketServer:
    def __init__(self, host='localhost', port=12345,):
        self.host = host
        self.port = port
        self.server_socket = None
        self.minions = load_minions()

    def start_server(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Game server started, waiting for connections...")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        buffer = ''
        try:
            i = 0
            while True:
                i+=1
                print(f"i: {i}")
                data = client_socket.recv(8192).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.startswith("@"):
                        line = line[1:]  # Remove "@"
                        index_and_data = line.split("¨", 1)
                        if len(index_and_data) == 2:
                            index_str, minion_data = index_and_data
                            index = int(index_str)
                            print(f"Received minion data for index {index}")
                            minion_dict = ast.literal_eval(
                                minion_data.replace('null', "None").replace("true", "True").replace("false", "False"))
                            minion = Minion.from_dict(minion_dict)
                            minion.save_to_text()
                            # Include index when sending back data with delimiter
                            response = f"{4-index}¨{minion.to_custom_string()}\n"
                            self.send_data(client_socket, response)
                        else:
                            print("Invalid data format received.")
                    elif line.startswith("set_minions"):
                        print("Received request to send back minions.")
                        self.minions = load_minions()
                        response = ""
                        for i, minion in enumerate(self.minions):
                            response += f"{i}¨{minion}\n"
                        self.send_data(client_socket, response)


        except ConnectionResetError as e:
            print(e)
        finally:
            client_socket.close()
            print("closed")

    @staticmethod
    def send_data(client_socket, message):
        try:
            message_with_delimiter = message + '\n'  # Append newline as a delimiter
            client_socket.sendall(message_with_delimiter.encode('utf-8'))
            print(f"Sent data: {message_with_delimiter}")
        except Exception as e:
            print(f"Failed to send data: {e}")


if __name__ == "__main__":
    server = GameSocketServer()
    server.start_server()
