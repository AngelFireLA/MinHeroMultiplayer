#This file exclusively interacts with the SWF (through the policy server)
# Also connects to the GameServer
#This acts as a "transformer" between the Actionscript within the SWF, and the multiplayer transmission system


#imports
import random
import time
import subprocess
from policy_server import serve_policy #auto-run the policy server
from GameServer import GameSocketServer #auto-run the GameServer
from sys import exit as exitt


from min_hero_classes import Minion, BaseMinion, Gem #class structures for Min Hero items
import os
import socket
import threading
import ast
from constants import * #all constants

class Client():
  def __init__(self,GameServerAddress,GameServerPort,SWFServerPort,SWFServerAddress,username):
    """The Client class is the data object used to store the connections between the GameServer and between the policy server"""
    #client-specific data
    self.username = username
    self.ID = None #get assigned an ID on confirmation of connection
    self.minions = []
    self.time_since_team_update = time.time() #time taken to update
    self.currSelectedMove = None    #placeholders for the last move to be able to re-send on packet send error
    self.currSelectedTargets = None
    self.flags = [] #any extra things to process. Status changes that may occur

    
    #CONNECTION SETUP
    self.ConnectedToGameServer = False
    self.GLOBAL_EXIT = False #when set to true, delete thyself
    self.ConnectedToSWF = False
    self.GSCarousel = {} #a dictionary that contains all the successfully received message data from the GameServer from each MsgType to be processed
    self.SWFCarousel = {}#a dictionary that contains all the successfully received message data from the SWF for each MsgType to be processed.
    #setup using constants
    for itm in all_msgtype_GS:
      self.GSCarousel[itm] = None
    for itm in all_msgtype_SWF:
      self.SWFCarousel[itm] = None

    #connect to GameServer
    try:    
      self.GameServerSocket = socket.socket()
      self.GameServerSocket.connect((GameServerAddress,GameServerPort))
      self.ConnectedToGameServer = True
      success("Connected to GameServer!")
    except:
      raise ConnectionRefusedError("Unable to connect to GameServer!! Try checking if the server is running on the right ports")
    #create the SWFSocket server
    info("Starting SWFServer")
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((SWFServerAddress, SWFServerPort))
    self.server_socket.listen(2)
    info("SWFServer created! Waiting for SWF to connect (press 'Play')")
    self.SWFSocket, self.SWFaddr = self.server_socket.accept() #we know the first game to connect MUST be the one!
    self.ConnectedToSWF = True
    info(f"SWF file connection from {self.SWFaddr}")
    
    success("Ready to play!")
    self.main()

  def main(self):
    """The main loop that the Client.py executes. This is when we actually "begin" the client
    This relies on having extensive knowledge on how the turn order works both within the SWF and the GameServer, in order to perfectly capture the required data at the right moment.
    There are technically 4 threaded instances: The send and receive for the GameServer, and the send/receive for the SWFServer
    """   
    #SETUP
    #threading.Thread(target=self.receive_GameServer).start() #run GameServer receiver async
    threading.Thread(target=self.receive_SWF).start() #run SWF receiver async
    while True:
      """PROCESSING STAGE
      This is where the data collected from the receivers is accessed, and then processed as needed into the correct variables. It's done here because it reduces the overhead needed within the receivers.
      This also handles all the sending needed. There should always be some kind of result, and usually sending a message complete a "cycle".
      """
      pass

  def receive_GameServer(self,*args):
    """The threaded function that receives from the GameServer, and processes accordingly"""
    while self.ConnectedToGameServer: #whilst we are able to receive
      try:
        datas = self.SWFSocket.recv(16384).decode().split(split_order[0]) #receive, decode and process block into message(s). Will fail if bad data
      except:
        warn(f"Bad data received!")
        datas = [split_order[1]]
        self.ConnectedToGameServer = False
      """
      GAMESERVER -> CLIENT
      (messages from the GameServer towards the client)
      The client should ideally:
      * send a message back to the GameServer using send_GameServer to confirm
      * process the received data into Pythonic structures
      * send a message onto the SWF (if needed)
      """
      for message in datas: #for each message (usually one, might end up as multiple if processing goes bad)
        try:
          big_dat = message.split(split_order[1])
          MsgType = big_dat[0]
          data = big_dat[1:]
        except:
          MsgType = "NONONONONO"
          pass  #man I can't keep writing edge cases888
        if MsgType == "NONONONONO":
          error("Brwoken")
        elif MsgType == "playerTeamDump":
          all_minions = data
          with open("minion_export_current.txt","w") as foile:
            for minion in all_minions:
              foile.write(minion+"\n")
          success("All minions are received successfully! Check 'minion_export_current.txt'.")
        else:
          error("This should not be triggering: check data:")
          error(f"{MsgType}:{data}")

  def send_GameServer(self,msg:str):
    """ The function that is instantaneously called to send something to the GameServer
        Possibly update to include data formatting in this function (i.e params of MsgType, data)
    """
    try:
      self.GameServerSocket.send(msg.encode())
    except ConnectionResetError:
      error("GameServer connection has closed")
    info(f"Sent: {msg}")

  def receive_SWF(self,*args):
    """The threaded function that receives from the SWF, and processes accordingly."""
    while self.ConnectedToSWF: #whilst we are able to receive
      try:
        datas = self.SWFSocket.recv(16384).decode().split(split_order[0]) #receive, decode and process block into message(s). Will fail if bad data
        #print(datas)
      except:
        warn(f"Bad data received!")
        datas = [split_order[1]]
        self.ConnectedToSWF = False
      """
      SWF -> CLIENT
      (messages from the SWF towards the client)
      The client should ideally:
      * send a message back to the SWF using send_SWF to confirm a message
      * process the received data into Pythonic structures
      * send a message onto the GameServer (if needed)
      """
      for message in datas: #for each message (usually one, might end up as multiple if processing goes bad)
        try:
          big_data = message.split(split_order[1])
          MsgType = big_data[0]
          data = big_data[1:]
        except:
          warn("Data is not of proper format! Assuming it's a 'bald' string (possibly as part of a data pack)")
        if MsgType == "playerTeamDump": #CURRENT MINION LOADOUT IS EXPORTED
          all_minions = data
          for mini in all_minions: info(mini)
          success("Received a minion dump!")
        elif MsgType =="" and data ==[]:
          error("Blank data due to connection close, exit")
          self.GLOBAL_EXIT = True
          del self
          exitt()

        else:
          error("This should not be triggering, check data:")
          error(f"{MsgType}:{data}")


  def send_SWF(self,msg:str):
    """ Function that sends the message towards the actual game.
        Currently just sends whatever
        Possibly split parameter for code, payload like I did with Formula Gun""" 
    try:
      self.SWFSocket.send(msg.encode('utf-8'))
      info(f"Sent data: {msg}")
    except Exception as e:
      error(f"Failed to send data: {e}")


def autorun_flash_file(cmd, arg):
  """Run a Flash file, with the 'cmd' being the path to the Flash Projector, and the 'arg' being the SWF file"""
  result = subprocess.run([cmd, arg], capture_output=False, text=True)
def autorun_exe(*args):
  """Run a Flash game as an exe"""
  cmd = "".join(args)
  result = subprocess.run([cmd], capture_output=False, text=True)

if __name__ == "__main__": #this is the file to run!
  threading.Thread(target=serve_policy).start() #run policy server async
  info("Policy server running..")
  if IS_SERVER: #if we are the server
    game_srv = GameSocketServer(GAME_SERVER_ADDRESS,GAME_SERVER_PORT)
    threading.Thread(target=game_srv.start_server).start()
    info("Game Server running..")
  if AUTO_RUN_FLASH: 
    #threading.Thread(target=autorun_exe, args=(FLASH_PATH)).start() #run MH exe async 
    threading.Thread(target=autorun_flash_file, args=(FLASH_PATH, "default.swf")).start() #run MH SWF async
    info("Game running..")
  cloint = Client(GAME_SERVER_ADDRESS,GAME_SERVER_PORT,POLICY_SERVER_PORT,POLICY_SERVER_ADDRESS,
         username="test")
  



"""
HOW THIS WORKS:

The POLICY SERVER is a server that provides the tunnel between a specified port and the game itself.
It basically says "this SWF will send/receive at the port specified within the policy". This is port 12345 (the Policy Port).

The CLIENT is a server and a client. It is a client in the multiplayer system (client to GameServer), but is also the server at the Polciy Port
This means that it can send/receive data towards the SWF as if the client *is* a server, yet this data can then be used as data to send/receive to the GameServer as part of a multiplayer system.

The GAMESERVER is the server that handles the multiplayer game state, and the connection between both clients. For now, this can be a hard-set server where we receive particular prompts from the client.py and simulate an accurate response.

Essentially, we are using a "trigger" system extended through 3 stages:

target SWF is currently in "waiting mode" i.e it has paused gameplay until a result is confirmed. Essentially the perspective of the NPCs when we are deciding the move.
current SWF makes a decision -> 
* calculates the result of any "random" initial criteria (i.e chance of multi-targets, chance of speed buff/debuff, chance of exhaust)
* Account for a critical chance as well. We are basically performing full execution up until the resolution of abilities
* sends to client.py and waits for confirmation
client.py processes the decision 
* sends to GameServer
* updates local variables to store the last executed move
GameServer processes decision 
* updates local image of both
* sends to both client.py and target client.py
both client.py process the result
* target client.py updates their variables
* send to their SWF
both SWF execute:
* both progress past their waiting blocks, and can now execute the move
* execution used the fixed random probabilities found from current SWF
* finalisation (MoveStones)
* Then, both SWF can save a "teamDump" that can be used to sync both sides
both SWF send round update
* both client.py do last update of variables to reflect their current team state
* client.py both forward to the GameServer
* GameServer can utilise a "flip-flop" function to make both teams from the same perspective. These should match up.
GameServer verifies fair completion
* If the two backups are the same, GameServer sends "ok" message back to both client.py, as well as any required update data
* Both client.py send back to their SWF. Received data calculates the new turn oreder
* If there is a DIFFERENCE between them (which shouldn't happen, but can't be too safe!), then prioritise the current SWF
* Using the flipped backup, send back to misbehaving client.py. This then performs a full reset over the current layout.

BIG QUESTION: how do we communicate between the different components
ANSWER: Class. even through the functions are threaded, *they can still interact with the Client class*.
This allows us to create a "carousel" where we update a particular variable with the right data, which is then passed elsewhere.
Almost like a cohesive system of 4 functions, where each one calmly notifes the others of their result/intention, and then able to resolve.

BIG QUESTION: Why do we need to perfectly time stuff on Actionscript side:
ANSWER: I really cannot be asked to learn how to create an asynchronus loop within Actionscript. Therefore, it's better to rely on Python (strong suit) as opposed to Actionscript. The beauty of being turn-based is that there are clear, defined points. 
Additionally, we can through blocking waits wherever, and use dummy "confirm" messages to give us a system where the SWF listens when we want, and sends when we need it.

"""
  
