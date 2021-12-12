# For all REST API configurations
import requests
import json

# For file information parsing
import re

# For back-up folder name automation
import datetime

# For directory traversal and terminal command calls 
import os
import subprocess
import time

# For downloaded file integrity check
import hashlib

# Regex for different information in the jar file
jar_version_regex = r"\d\.\d+\.?\d?"
jar_build_regex = r"\d+\.jar"

# Base link for the PaperMC API
paperOrigin = "https://papermc.io/api/v2/projects/paper/"

# Initialize current jar file information
current_jar_name = ""
current_version = ""
current_build = 0

# Initialize latest jar file information
latest_link = ""
latest_jar_name = ""
latest_hashcode = ""

# Returns a string containing the path a given amount of directories above the given directory
def go_up_directory(directory, amount):
    # Make a list of all the directories leading up the given one, cleaning up the empty values just in case something weird happens
    items = directory.split("/")
    items = list(filter(lambda a: a != "", items))
    
    # Remove the amount of directories given (end to start)
    items = items[:-amount]

    # Create the new directory path (string?)
    new_dir = ""
    for path in items:
        new_dir += "/" + path

    return new_dir

# Automated directories
py_dir = os.path.dirname(os.path.realpath(__file__))
server_dir = go_up_directory(py_dir, 1)
backup_dir = go_up_directory(server_dir, 1) + "/minecraft-backups"

# Starts the paper minecraft server
def start_server():
    # Attempt to start the screen session for the server
    subprocess.run("scripts/start.sh", cwd=server_dir, shell=True)
    print("-> Server started")

# Stops the paper minecraft server
def stop_server():
    # Send the stop command
    subprocess.run("screen -S mcServer -p 0 -X stuff 'stop^M'", shell=True)

    # Wait until the server is fully closed
    while True:
        if(subprocess.call("screen -ls | grep mcServer", shell=True, stdout=subprocess.DEVNULL) == 1):
            break 
        print("-> Waiting for server to shutdown...")
        time.sleep(1)

    print("-> Server shutdown")

# Backs up the minecraft server world
def back_up_server():
    # Create a folder for the latest back-up
    if(os.path.exists(backup_dir)):
        # Generate the back-up folder name and directory
        folder_name = datetime.date.today().strftime("%b-%d-%Y")
        folder_dir = backup_dir + "/" + folder_name

        # Create the back-up folder
        if(os.path.exists(folder_dir)):
            # If for some ungodly reason time turns back and repeats itself then just delete the folder and remake it :)
            subprocess.run("rm -r " + folder_dir, cwd=backup_dir, shell=True)
            os.mkdir(folder_dir)
        else:
            os.mkdir(folder_dir)

        # Back-up all world dimensions in the folder made above
        # NOTE If you use a custom world name, change the "world" in line 102 to your custom world name
        for file_name in os.listdir(server_dir):
            if re.match("world", file_name):
                subprocess.run("cp -R " + file_name + " " + folder_dir , cwd=server_dir, shell=True)
                print("-> Backed up " + file_name)

        # Remove folders older than 2 weeks
        for folder_name in os.listdir(backup_dir):
            # Get the current folder date (if there is any) and set a time limit of 14 days ago
            try:
                folder_date = datetime.datetime.strptime(folder_name, "%b-%d-%Y")
            except:
                continue

            date_limit = datetime.datetime.now() - datetime.timedelta(days=14)

            # Compare dates and if the folder date is older than the limit remove it
            if(date_limit > folder_date):
                subprocess.run("rm -r " + folder_name, cwd=backup_dir, shell=True)
    else:
        # Create the back-up directory and re-call the function so that it creates the folder and stores the backups
        os.mkdir(backup_dir)
        back_up_server()

# Inhabits the current version global variables with their respective information
def get_current_info():
    for file_name in os.listdir(server_dir):
        if file_name.endswith(".jar"):
            # Inhabit the current .jar file name global variable
            global current_jar_name
            current_jar_name = file_name

            # Inhabit the current server version global variable
            global current_version
            current_version = re.search(jar_version_regex, file_name).group()

            # Inhabit the current build global variable
            global current_build
            current_build = re.search(jar_build_regex, file_name).group().replace(".jar", "")

# Returns the last value of a given key from a JSON provided by the PaperMC API
def get_last_value_in_key(jsonData, key):
    vArray = jsonData[key]
    return vArray[len(vArray) - 1]

# Returns the corresponding information in JSON from the PaperMC API
def get_json_from_api(route):
    response = requests.get(paperOrigin + route)
    return response.json()

# Inhabits the latest version  global variables (from the PaperMC API) with their respective information
def get_api_info():
    # Get the available versions of Minecraft from PaperMC
    aVJSON = get_json_from_api("")
    latestVersion = get_last_value_in_key(aVJSON, "versions")
    print("The latest available Minecraft version from PaperMC is: " + latestVersion)
    
    # Get the available builds of the latest version of Minecraft from PaperMC
    aBJSON = get_json_from_api("versions/" + latestVersion)
    latestBuild = get_last_value_in_key(aBJSON, "builds")
    print("The latest build of this version is: " + str(latestBuild))

    # Get the latest build information/description
    lBDesc = get_json_from_api("versions/" + latestVersion + "/builds/" + str(latestBuild))
    
    # Inhabit the latest .jar file name global variable
    global latest_jar_name 
    latest_jar_name = lBDesc['downloads']['application']['name']
    

    global latest_hashcode
    latest_hashcode = lBDesc['downloads']['application']['sha256']

    # Create the download link for the lastest PaperMC version and build
    link = paperOrigin + "versions/" + latestVersion + "/builds/" + str(latestBuild) + "/downloads/" + latest_jar_name

    return link

# Returns True if the latest version (from the API) is newer than the current version
def latest_is_newer():
    latest_version = re.search(jar_version_regex, latest_jar_name).group()
    latest_build = re.search(jar_build_regex, latest_jar_name).group().replace(".jar", "")

    # If the versions differ and the latest version is larger than the current version, then yes, the latest is newer
    if(current_version != latest_version and latest_version > current_version):
        return True
    # Otherwise if the versions are the same but the latest build is bigger than the current, then yes, the latest is newer
    elif(current_version == latest_version and latest_build > current_build):
        return True
    
    # If current is equal to latest, or for some reason current is newer than latest then return false
    print("-> Current version >= API version\n")
    return False

# Updates the current 
def update_sh(jar_name):
    # Read throughout the file, copy the contents into a variable and update the JAR file name within that variable
    sh_script = open(py_dir + "/" + "start.sh", "rt")
    code = sh_script.read()
    code = code.replace(server_dir + "/" + current_jar_name, server_dir + "/" + latest_jar_name)
    sh_script.close()

    # Rewrite the file with the variable that contains the new JAR file name
    sh_script = open(py_dir + "/" + "start.sh", "wt")
    sh_script.write(code)
    sh_script.close()

# Updates the server JAR file alongside everything that references it
def update_server():
    # Trigger a download of the latest JAR file, wait until it is done downloading and verify its integrity (by hashing it and comparing hashes)
    subprocess.run("wget " + latest_link, cwd=server_dir, shell=True)
    download_hash = hashlib.sha256(open(server_dir + "/" + latest_jar_name, "rb").read()).hexdigest()

    # If both hashes are identical
    if(latest_hashcode == download_hash):
        # Delete the current JAR file
        subprocess.run("rm " + current_jar_name, cwd=server_dir, shell=True)

        # Update the current JAR file in start.sh with the latest JAR file
        update_sh(latest_jar_name)
    else:
        # Delete the downloaded JAR file and try again
        subprocess.run("rm " + latest_jar_name, cwd=server_dir, shell=True)
        update_server()

# Update the current version global variables
get_current_info()
print("Current version info:")
print("-> Version: " + current_version)
print("-> Build: " + str(current_build))
print("-> JAR: " + current_jar_name)
print("")

# Get information from the API
latest_link = get_api_info()
print("Link to this version: " + latest_link)
print("-> JAR: " + latest_jar_name + " \n-> SHA256: " + latest_hashcode)
print("")

# Stop the server for backup and updates
print("Shutting down the server...")
stop_server()
print("")

# Backup the server world
print("Backing up the server...")
back_up_server()
print("")

# Check for any updates and update if there is a newer version
print("Checking for updates...")
if(latest_is_newer()):
    print("-> Update found, updating server...")
    update_server()
    print("--> Server has been updated!")

print("Starting the server back up again...")
start_server()
