#!/usr/bin/python3

import requests
import time
import shutil
import os


checked_url = "https://www.archlinux.org"

def get_wallpaper():
    url = "https://api.nasa.gov/planetary/apod?api_key="

    with open("/home/karol/.config/nasa_wallpaper/nasa_api_key.txt", "r") as keyf:
        url += keyf.readline()
        url = url.replace('\n', '')

    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        picture_link = response["url"]
        picture_response = requests.get(picture_link, stream=True)
        with open("/home/karol/.wallpapers/nasa-wallpaper.jpg", "wb") as f:
            shutil.copyfileobj(picture_response.raw, f)

        double_nl = "\n\n"
        description = "Date: " + response["date"] + double_nl + "Title: " + response["title"] + double_nl + "Explanation: \n" + response["explanation"] + double_nl + "Link: " + picture_link + double_nl
        with open("/home/karol/.wallpapers/nasa_picture_description.txt", "w") as desc:
            desc.write(description)


while True:
    try:
        request = requests.get(checked_url)
        if request.status_code == 200:
            get_wallpaper()
            os.system("feh -B black --bg-center /home/karol/.wallpapers/nasa-wallpaper.jpg")
            break
        else:
            time.sleep(1)
    except requests.exceptions.ConnectionError:
        time.sleep(1)


