import os
import re
import requests
import sys
from bs4 import BeautifulSoup


def rename_files(directory, episodes):
    incomplete_pattern = re.compile("S[0-9]+\s")
    pattern = re.compile("S[0-9]+E[0-9]+]")
    for entry in os.listdir(directory):
        newname = entry
        if os.path.isdir(os.path.join(directory, entry)):
            rename_files(os.path.join(directory, entry), episodes)
            continue

        if re.search(pattern, entry):
            print(entry + " already labelled")
            continue

        if re.search(incomplete_pattern, entry):
            newname = re.sub(incomplete_pattern, '', entry).strip()

        for label in episodes:
            if filter_name(newname) in filter_name(episodes[label]):
                newname = label + " - " + episodes[label]
                print(entry + " renamed to " + newname)
                os.rename(os.path.join(directory, entry),
                          os.path.join(directory, newname))
                break


def filter_name(name):
    name = re.sub(".(mp4|avi|mpg|mkv)", "", name)
    name = re.sub("[\,\'\.\[\]\!\?\:\-]*", "", name)
    name = re.sub("([\s]{2,})*", " ", name)
    name = name.strip().lower()
    return name


if __name__ == "__main__":
    url = "https://thetvdb.com/series/%name%/allseasons/dvd"
    series_name = sys.argv[1]
    url = url.replace("%name%", series_name)

    directory = os.getcwd()
    if len(sys.argv) > 2:
        directory = sys.argv[2]

    page = requests.get(url)
    if page.status_code != 200:
        url = url.replace("/dvd", "/official")
        page = requests.get(url)

    soup = BeautifulSoup(page.content, "lxml")

    episodes = {}
    for title in soup.find_all("h4", class_="list-group-item-heading"):
        title = str(title)
        title = re.sub('<.*?>', '', title)
        content = re.findall("[0-9A-Za-z][0-9A-Za-z ,.!?';:]+", title)
        episodes[content[0]] = content[1]

    rename_files(directory, episodes)
