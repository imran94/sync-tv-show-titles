import os
import re
import requests
import sys
from bs4 import BeautifulSoup


def rename_files(directory, episodes):
    incomplete_pattern = re.compile("S[0-9]+\s")
    pattern = re.compile("S[0-9]+E[0-9]+]")
    for entry in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, entry)):
            print(entry + " is directory")
            rename_files(os.path.join(directory, entry), episodes)
            continue

        if re.search(pattern, entry):
            print(entry + " already labelled")
            continue

        if re.search(incomplete_pattern, entry):
            print(entry, end='')
            entry = re.sub(incomplete_pattern, '', entry).strip()
            print(" renamed to " + entry)

        name = re.sub(".(mp4|avi|mpg|mkv)", "", entry)
        for label in episodes:
            if name.lower() in episodes[label].lower():
                print(label + " - " + entry)
                episodes.pop(label)
                break

url = "https://thetvdb.com/series/%name%/allseasons/official"
series_name = sys.argv[1]
url = url.replace("%name%", series_name)

directory = os.getcwd()
if len(sys.argv) > 2:
    directory = sys.argv[2]

page = requests.get(url)
soup = BeautifulSoup(page, "lxml")

# with open("html.txt", "r") as f:
#     soup = BeautifulSoup(f, 'lxml')

episodes = {}
for title in soup.find_all("h4", class_="list-group-item-heading"):
    title = str(title)
    title = re.sub('<.*?>', '', title)
    content = re.findall("[0-9A-Za-z][0-9A-Za-z ,.!?';:]+", title)
    episodes[content[0]] = content[1]

print("Episode length before: " + str(len(episodes)))
rename_files(directory, episodes)
print("Episode length before: " + str(len(episodes)))

