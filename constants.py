#JUST like in my multi game "Formula Gun", I will keep all important constants here.
#This prevents clutter within the "client.py"

#imports
from colorist import red,yellow,green,blue,Color #colouring the input


#DEBUG PRINT SYSTEM
ALL_LEVELS = ["info","warning","none"] #all the different debug levels
DEBUG_LEVEL = "info" #current debug level

def error(msg,colour="red"):
  """Print an error message in specified colour (default=red). Lowest debug level, fatal error within code. Expected to cause an execption within main code"""
  try:   Colour(colour,mode=0)(msg)
  except:red("BAD ERROR PRINT INPUT")
def warn(msg,colour="yellow"):
  """Print a warning message, but continue executing code. Used at the 'warning' level"""
  global DEBUG_LEVEL
  if DEBUG_LEVEL != "none":
    try:   Colour(colour,mode=0)(msg)
    except:red("BAD WARNING PRINT INPUT")
def success(msg,colour="green"):
  """Print a success message in specified colour (green). Always used"""
  try:   Colour(colour,mode=0)(msg)
  except:red("BAD SUCCESS PRINT INPUT")
def info(msg):
  """Basic print module, renamed to be included in the print debug level system. Used at the 'info' level"""
  global DEBUG_LEVEL
  if DEBUG_LEVEL=="info": print(msg)
def Colour(colour="reset",mode=1): #-> returns function for mode0 and escape sequence for mode1 (use reset to complete escape code)
  """Find the appropiate function or escape code from 'colorist' module"""
  if mode==0: #looking for a function
    if colour == "red": return red
    elif colour == "yellow": return yellow
    elif colour == "green": return green
    elif colour == "blue": return blue
    else: return 0
  elif mode==1: #looking for escape code
    if colour == "reset": return Color.OFF
    elif colour == "red": return Color.RED
    elif colour == "yellow": return Color.YELLOW
    elif colour == "green": return Color.GREEN
    elif colour == "blue": return Color.BLUE
    else: return 0

#SERVER CONFIG

AUTO_RUN_FLASH = True           #do we run the Flash game with this (preferred to reduce time)
FLASH_PATH = ".\\Flash.exe"      #path to flash exe. This can be the projector OR the converted EXE
GAME_SERVER_ADDRESS = "127.0.0.1"#address that the GameServer is on
GAME_SERVER_PORT = 8181          #and the port
POLICY_SERVER_ADDRESS = "127.0.0.1"#address of the client server
POLICY_SERVER_PORT = 12345       #port of the client server (as defined in the policy_server)
IS_SERVER = True                 #is this program the GameServer as well?











#NETWORK PROTOCOLS
#these define the messages that are allowed as network messages. This means we handle data EXACTLY as we expect and need
all_msgtype_SWF = [ "backup", #BACKUP message: Will contain the defined layout for the whole level. Sent for archival
                    "log", #LOG message: Contains the message to write to a log file
                    "move", #MOVE message: Contains the selected move, as well as the targets, and calculated probabilities
                    "update",#STATUPDATE message: contains a minion which has had a particular status change applied (i.e unfrozen, unstunned)
                    "waiting", #WAITING message: notification that the SWF is paused until message received.
                    "confirm", #CONFIRM message: notification that the SWF has successsfully loaded and received data. Use for important, lengthy data (.e backup loading)
                    "teamExport", #TEAMEXPORT message: Contains the loadout of 5 minions
                    ""]
#a list of all the possible message codes useable from GameServer to client
all_msgtype_GS = [  "backup", #BACKUP message: Contains a defined layout for the whole level. Only sent for replacement
                    "waiting",#WAITING message: notification that the GameServer is waiting for the next message
                    "resend", #RESEND message: in the case of not being able to process, request the last message to be sent again.
                    "move",#MOVE message: the opponent has selected their move, and 
                    "update",#UPDATE message: the opponent has had one of their minions updated from a passive effect
                    ""] 

#the above two can be merged as they basically cover similar things. Just add a flag for the type of mode
#the Deliminator Series, the method to split strings such that their content can be used. Currently I'm using whatever I like, but once the "actual" ones are known, swap as needed. Hard-coding is also possible!
split_order = [   
              ">", #1st: used to overcome buffer issues. Suffix to every message. Split by this to get each message
              "$$", #2nd: used to identify the MessageType. Split by this to get the ("type", "data") list
              "#", #3rd: used to split the data into several parts. Optional. Split by this to get each bit of data as [item1, item2..]. Actual length known from Message Type
              ]

#Possible "flags" raised by the SWF to denote a particular update within a minion
all_update_flags = [
  "unfrozen", "unstun", #-> explanatory, minion has broken free randomly
]

