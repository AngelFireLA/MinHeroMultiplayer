In-work project of bringing pvp battles to Min hero Tower of Sages

You can export your team as text files to share them, and you can also import enemy teams from these files, or from other connected clients if you know their username.

## How to use
(0. Install python 3.11 and be sure to tick the box "Add Python to PATH" during the installation on the first screen of the installer, at the bottom)
1. Download the project and extract it
2. Open two terminals in the project folder
3. On the first one run the command 'python policy_server.py'
4. On the second one run the command 'python server.py'
5. Run the start.bat to build the modded exe
6. Go in config.txt and pick a unique username.
6. Run the generated Flash.exe
7. Enjoy (you will have to do steps 2 to 4 each time)

## How to export my team
1. Open your settings while in a save
2. Toggle "Export Team"
3. Done, your team's minions' files are saved in the "minions" folder (one file per minion)

## How to import a team from files
(0. Be sure to have followed the usage steps)
1. Get the files of the 5 minions you want to import
2. Put them in the "active_minions" folder while also removing any other file in it
3. Open config.txt and change "target" to be the same as your username
4. Relaunch the modded exe file
5. Toggle "Load Enemy" in the settings
6. Done, your team is now imported

## How to import a team from another client
(0. Be sure to have followed the usage steps)
1. Get the username of the client you want to import the team from
2. Be sure they have exported their team since the server's last restart
2. Open config.txt and change "target" to be the same as the username of the client you want to import the team from
4. Relaunch the modded exe file
5. Toggle "Load Enemy" in the settings
6. Done, their team is now imported


## How to fight an imported team
(0. Be sure to have followed the usage steps and have followed the import team steps)
1. Go to the Lobby
2. Talk to the NPC protecting the titan egg (the one higher).
3. This will start the battle, enjoy ! (be sure to save before engaging in a battle as it's still experimental)
