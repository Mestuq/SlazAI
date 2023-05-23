#!/bin/bash
cd /home/pi/files
git config --global --unset http.proxy 
git reset --hard
git pull origin master
git push origin master
chmod +x run_update.sh
chmod +x run_bot.sh
python3 index.py