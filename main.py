# Based on https://stackoverflow.com/questions/29266605, https://stackoverflow.com/questions/38309395

print("Initializing...")

from os import system, environ, walk
from os.path import join
import heroku3
import tarfile
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET

system("git config --global user.name \"annotation-extract-bot\"")
system("git config --global user.email annotation-extract-bot@annotation-extract-bot.local")

url = environ["url"] # ex https://archive.org/download/youtubeannotations_00/A-.tar
item = environ["url"].split("/")[-1].split(".")[0]

print("Downloading tar file (this may take a while)...")
urlretrieve(url, url.split("/")[-1])

print("Extracting tar file...")
tar = tarfile.open(url.split("/")[-1])

vidsl = set()
urlsl = set()

# https://stackoverflow.com/a/19587581
for file in tar:
    if file and tar.extractfile(file):
        urls = ET.fromstring(tar.extractfile(file).read()).getroot().findall('.//url')
        for tag in urls:
            urlint = tag.attrib['value']
            if urlint.startswith("https://www.youtube.com/watch?"):
                vidsl.add(urlint.split("v=")[-1].split("&")[0])
            else:
                urlsl.add(urlint.removeprefix("https://www.youtube.com/"))

system("git clone "+environ["git-url"]+" repo")
urlf = open("repo/"+item+"_urls.txt", "w")
for item in urlsl:
    urlf.write(item+"\n")
urlf.close()

vidf = open("repo/"+item+"_vids.txt", "w")
for item in vidsl:
    vidf.write(item+"\n")
vidf.close()

system("cd repo; git add .; git commit -m \"Add "+item+"\"; git push")
heroku3.from_key(environ['heroku-key']).apps()[environ['heroku-app']].scale_formation_process('worker', 0)
