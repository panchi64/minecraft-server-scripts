#!/bin/sh
# Change the [path/to/jar] to the path where the minecraft server jar is located
screen -d -m -S mcServer java -Xms2G -Xmx8G -jar [/path/to/jar/]paper-1.18-57.jar --nogui
