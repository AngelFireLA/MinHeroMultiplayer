import random
import time

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
        self.clients = {}

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
        def sendMove(player_username, target_username, move, targets):
            # wait 1 second
            time.sleep(1)
            current_client = self.clients[player_username]
            client_socket = current_client.client_socket
            if target_username == current_client.username:
                print("Sending Move")
                self.send_data(client_socket, "%move:-1#%targets:-1")
            else:
                # targets are separater by a | with the target tuple's content separated by _
                targets_str = "|".join([f"{target[0]}_{target[1]}" for target in targets])
                response = f"%move:{move}#%targets:{targets_str}"
                time.sleep(1)
                self.send_data(client_socket, response)
                print(f"Successfully sent move to client {player_username}.")

        buffer = ''
        current_username = None
        try:
            i = 0
            current_client:Client = None
            target_username = None
            target_client:Client = None
            while True:
                i+=1
                print(f"i: {i}")
                data = client_socket.recv(8192).decode('utf-8')
                print(data)
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    time.sleep(0.1)
                    line, buffer = buffer.split('\n', 1)
                    if line.startswith("@login:"):
                        username = line.split("@login:")[1]
                        if username in self.clients:
                            raise ValueError("Two clients with the same name tried to connect")
                        current_client = Client(username, client_socket)
                        self.clients[username] = current_client
                        current_username = username
                        print(f"New Client of username {username} connected.")
                    elif line.startswith("@"):
                        line = line[1:]  # Remove "@"
                        index_and_data = line.split("¨", 1)
                        if len(index_and_data) == 2:
                            if current_client.minions:
                                if time.time() - current_client.time_since_team_update > 5 or len(current_client.minions) == 5:
                                    current_client.minions = []
                                    current_client.time_since_team_update = time.time()
                            index_str, minion_data = index_and_data
                            index = int(index_str)
                            print(f"Received minion data for index {index}")
                            minion_dict = ast.literal_eval(
                                minion_data.replace('null', "None").replace("true", "True").replace("false", "False"))
                            minion = Minion.from_dict(minion_dict)
                            minion.save_to_text()
                            current_client.minions.append(minion)
                            current_client.time_since_team_update = time.time()
                        else:
                            print("Invalid data format received.")
                    elif line.startswith("set_minions"):
                        print("Received request to send back minions.")
                        self.minions = load_minions()
                        response = ""
                        for i, minion in enumerate(self.minions):
                            response += f"{i}¨{minion}\n"
                        self.send_data(client_socket, response)
                    elif line.startswith("receive_minions_from"):
                        target_username = line.split(" ")[1]
                        if target_username == current_client.username:
                            print("Received request to send back minions.")
                            self.minions = load_minions()
                            response = ""
                            for i, minion in enumerate(self.minions):
                                response += f"{i}¨{minion}\n"
                            self.send_data(client_socket, response)
                        else:
                            if target_username in self.clients and self.clients[target_username].minions:
                                target_client = self.clients[target_username]
                                response = ""
                                for i, minion in enumerate(target_client.minions):
                                    response += f"{i}¨{minion.save_to_text()}\n"
                                self.send_data(client_socket, response)
                                print(f"Successfully receieved minions from target client {target_username}.")
                            else:
                                print(f"Target client {target_username} doesn't exist or doesn't have any minion loaded.")
                    elif line.startswith("send_minions_to"):
                        target_username = line.split(" ")[1]
                        if target_username in self.clients:
                            target_client = self.clients[target_username]
                            response = ""
                            for i, minion in enumerate(current_client.minions):
                                response += f"{i}¨{minion.save_to_text()}\n"
                            self.send_data(target_client.client_socket, response)
                    elif line.startswith("||battle:pick_move"):
                        #we get the move separated by a space
                        current_client.current_battle_move = line.split(" ")[1]
                        print("Minion move: ", current_client.current_battle_move)
                    elif line.startswith("||battle:pick_targets"):
                        # we get the targets separated by a space
                        targetsStr = line.split(" ")[1]
                        # each target is a number, separated by #
                        current_client.targets = [
                            segment.split("_")
                            for segment in targetsStr.split("#")
                            if len(segment.split("_")) == 2
                        ]
                    elif line.startswith("||battle:send_move"):

                        if target_client.current_battle_move and target_client.targets:
                            sendMove(current_username, target_username, target_client.current_battle_move, target_client.targets)
                            target_client.current_battle_move = None
                            target_client.targets = None
                        else:
                            print(f"{i} could not send move, retrying in 1 second")
                            time.sleep(3)
                            self.send_data(client_socket, "%plzresend")

        except ConnectionResetError as e:
            print(e)
        finally:

            client_socket.close()
            print("closed")
            #remove username with the client_socket form self.clients
            keys = list(self.clients.keys())
            for username in keys:
                if username == current_username:
                    del self.clients[username]

    @staticmethod
    def send_data(client_socket, message):
        try:
            message_with_delimiter = message + '\n'  # Append newline as a delimiter
            client_socket.sendall(message_with_delimiter.encode('utf-8'))
            print(f"Sent data: {message_with_delimiter}")
        except Exception as e:
            print(f"Failed to send data: {e}")


class Client:
    def __init__(self, username, client_socket):
        self.username = username
        self.client_socket = client_socket
        self.minions = []
        self.time_since_team_update = time.time()
        self.current_battle_move = None
        self.targets = None

if __name__ == "__main__":
    server = GameSocketServer(host="0.0.0.0")
    server.start_server()
