In-work project of bringing pvp battles to Min hero Tower of Sages

this is square_nine's variant version, that aims to remove the clutter of batch files and provide the SWF->Client->GameServer multiplayer pipeline

## How to use
(0. Install python 3.11 and be sure to tick the box "Add Python to PATH" during the installation on the first screen of the installer, at the bottom)
1. Download the project and extract it
2. Run "client.py". This will automatically launch the game as well (default.swf).

## How to export my team (NOT PORTED YET)
1. Interact with the Minion Manager dude in the lobby
2. Text file will be created in directory that the client.py file is in.

## How to import a team from files (NOT PORTED YET)
(0. Be sure to have followed the usage steps)
1. Get the files of the 5 minions you want to import
2. Name this file "enemy_to_import.txt"
3. When you interact with the MultiGuy, it'll load the team.

## How to import a team from another client (NOT PORTED YET)
(0. Be sure to have followed the usage steps)
1. Get the username of the client you want to import the team from
2. Be sure they have exported their team since the server's last restart
2. Open config.txt and change "target" to be the same as the username of the client you want to import the team from
4. Relaunch the modded exe file
5. Toggle "Load Enemy" in the settings
6. Done, their team is now imported

## How to fight an imported team (NOT PORTED YET)
(0. Be sure to have followed the usage steps and have followed the import team steps)
1. Go to the Lobby
2. Talk to the NPC protecting the titan egg (the one higher). He's "MultiGuy".
3. This will start the battle, enjoy ! (be sure to save before engaging in a battle as it's still experimental)

## I WANNA HELP!!!!
currently even I don't know what I'm doing. Join the Min Hero server https://discord.gg/ghCCAAb5Ed and DM me (square_nine) if you're interested (outlining what exactly you want to do).
