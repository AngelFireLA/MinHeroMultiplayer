import subprocess

import matplotlib
import numpy as np
from min_hero_classes import Minion, BaseMinion, Gem

import socket
import threading
import ast
matplotlib.use('Agg')  # Use a non-interactive backend


AUTO_RUN_FLASH =True #a constant to run Flash automatically
FLASH_PATH = 'D:\misc-flash\Adobe Flash Player 32.exe' #path to flash

def is_ally(minion_id, minions):
    for minion in minions:
        if minion["minion_id"] == minion_id:
            return minion["side"] == "ally"
    return False


def select_target_positions(minions, is_ally_turn):
    valid_positions = []
    for minion in minions:
        if minion["currHealth"] > 0:
            if (is_ally_turn and minion["side"] == "enemy") or (not is_ally_turn and minion["side"] == "ally"):
                valid_positions.append(minion["position"])
    return valid_positions


class GameSocketServer:
    def __init__(self, host='localhost', port=12345,):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Game server started, waiting for connections...")

        while True:
            try: 
                client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except: pass

    def handle_client(self, client_socket):
        move_ids = None
        minions = []
        minion_id = None
        action_pairs = {"playerTeamDump": "replaceCurrentTeam"} #a place to govern how to respond to certain data input. "the_type" of incoming data can cause a reaction detailed here.
        turn_count = 0
        try:
            while True:
                #receiving and processing data
                data = str(client_socket.recv(8192*2).decode('utf-8')) #large context window to receive
                if data != "":
                    print(data.replace('null', "None").replace("true", "True").replace("false", "False"))
                    #comment for use, as printing can take effort.
                else:
                    raise ValueError("Receiving blank data, check SWF") #ignore this error if you closed Flash Player before this
                data = data.split("$$")
                the_type = data.pop(0)
                #now to process the data depending on condition
                for item in data:
                    if the_type == "playerTeamDump" and turn_count==0: #converts current team into a list of Minion classes.
                        minion = Minion.from_dict(ast.literal_eval(item.replace('null', "None").replace("true", "True").replace("false", "False")))
                        minions.append(minion)
                #now that the data is processed how you want, any actions to do with it happen below
                turn_count+=1
                if the_type == "playerTeamDump": #dumps current team to txt file
                    with open("minions_dump-again.txt","w") as file:
                        for item in minions: file.write(item.to_custom_string() + "\n")
                #now to reply back with data
                for reaction in action_pairs.keys():
                    if reaction == the_type: #if we get a reaction for the type of data
                        the_type = action_pairs[reaction] #change the mode to what we want
                    else:
                        the_type = ""
                
                if the_type == "": pass #blank condition
                elif the_type == "replaceCurrentTeam": #replace the team
                    with open("D:/Min HEROOO/internet funsies/test/minions_dump.txt","r") as file: data = file.read() #get team data to replace with
                    data = data.replace("\n","$$") #format
                    self.send_data(client_socket, the_type + "$$" + data) #send it
               
                else: raise ValueError("Unrecognised reaction") #anything else

        except ConnectionResetError as e:
            print(e)
            pass
        finally:
            client_socket.close()
            self.server_socket.close()
            print("closed")

    @staticmethod
    def send_data(client_socket, message):
        try:
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent data: {message}")
        except Exception as e:
            print(f"Failed to send data: {e}")

def autorun(cmd, arg):
    result = subprocess.run([cmd, arg], capture_output=False, text=True)

if __name__ == "__main__":
    if AUTO_RUN_FLASH: 
        threading.Thread(target=autorun, args=(FLASH_PATH, "D:\Min HEROOO\internet funsies/test\default.swf")).start() #run MH async
        print("Game running..")
    server = GameSocketServer()
    server.start_server()
