# RUN CONTAINER IN INTERACTIVE MODE! 
# docker run -it slaz-AI

#Python environment
FROM python:3.9

#App workspace
WORKDIR /app

#Copying required files (extras not included!)
COPY files_conf/ app/files_conf
COPY slaz-AI/ app/slaz-AI

#Updating and installing firefox-esr (for youtube functionalities)
RUN apt-get update && \
    apt-get install -y firefox-esr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#Installing needed dependencies
RUN pip install python-discord selenium netifaces urllib3 configparser selenium

#Downloading geckodriver
RUN wget -O /usr/local/bin/geckodriver https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz && \
    tar -xvf /usr/local/bin/geckodriver -C /usr/local/bin 

#For non-desktop environments
ENV MOZ_HEADLESS=1
ENV DISPLAY=:99

#Path for geckodriver profile
ENV MOZ_PROFILE /files_conf/profile/

#Init new firefox profile (for Selenium)
RUN firefox-esr -CreateProfile default && pkill -9 firefox-esr

#Running bot and youtube initialisation
CMD  ["python", "slaz-AI/YoutubeInit.py"] && ["python", "slaz-AI/index.py"] 
