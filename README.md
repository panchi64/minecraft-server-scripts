# Installation
To use these scripts correctly please make sure you understand the following and have applied 4 things:
- The main server files are encompassed within a folder
- These scripts need to be contained within their own folder, named `scripts`, *within* the server files folder
- The python script will create a folder named 'minecraft-backups' right next to the folder where the server files are stored
- *These scripts are specifically made for servers using PaperMC*

1. Edit **line 25** of the `spigot.yml` file to say: `restart-script: ./scripts/start.sh`
2. In the `start.sh` script change the `/path/to/jar/` to the path where your minecraft server jar is found (also remove the brackets, they are there to help you identify what you have to change).
3. Make sure to install all python library dependencies, this can be done by using the following command:
   - `pip3 install [dependency]` (if pip3 doesn't work try with pip)
   - List of dependencies:
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

### Note
- The python script is written so the back-ups in the `minecraft-backups` folder are automatically deleted if they are older than 2 weeks.
- The chron job's minimum frequency *must* at least be daily, anything less than that and the backups for that day will be overriden.

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
