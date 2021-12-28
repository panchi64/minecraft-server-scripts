# Minecraft Server Automation Scripts
To use these scripts correctly please make sure you understand the following and have applied 4 things:
- The main server files should be placed within a folder (*see directory map example section for more detail*).
- The scripts need to be contained in their own folder, named `scripts`, *within* the server files folder.
- The python script will create a folder named `minecraft-backups` beside the folder where the server files are stored.
- The script will only provide a backup of the past 7 days, deleting any backups later than that time period.
- The script can be run as frequently as desired, however if run more than once a day it will overwrite that day's server backup.
- The script will update the server to the latest version and build provided by the API of PaperMC.
- *These scripts are specifically made for servers using PaperMC*

## Setup
1. Edit **line 25** of the `spigot.yml` file to say: `restart-script: ./scripts/start.sh`
2. In the `start.sh` script change the `/path/to/jar/` to the path where your minecraft server jar is found (also remove the brackets, they are there to help you identify what you have to change).
3. Make sure to install all python library dependencies, this can be done by using the following command:
   - `pip3 install [dependency]` (if pip3 doesn't work try with pip)
   - List of dependencies (some of these may "fail" because they come preinstalled with python):
      - request
      - json
      - re
      - packaging
      - datetime
      - os
      - subprocess
      - time
      - hashlib
4. Make a chron job that runs the python file whenever you want.

That's it :)

## Directory Map Example
- minecraft-backups/
- minecraft-server/
   - cache/...
   - libraries/...
   - logs/...
   - plugins/...
   - **scripts/**
     - **backup-and-update.py**
     - **start.sh**
   - versions/...
   - world/...
   - world_nether/...
   - world_the_end/...
   - banned-ips.json
   - banned-players.json
   - bukkit.yml
   - commands.yml
   - eula.txt
   - help.yml
   - ops.json
   - paper.yml
   - paper-1.x.x.jar
   - permissions.yml
   - server.properties
   - spigot.yml
   - usercache.json
   - version_history.json
   - whitelist.json
