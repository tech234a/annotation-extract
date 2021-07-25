# Based on https://stackoverflow.com/questions/29266605, https://stackoverflow.com/questions/38309395

print("Initializing...")

from os import system, environ
import heroku3, tarfile
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET
from time import sleep

#From https://github.com/iv-org/invidious/blob/ea0d52c0b85c0207c1766e1dc5d1bd0778485cad/src/invidious.cr#L79
CHARS_SAFE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

system("git config --global user.name \"annotation-extract-bot\"")
system("git config --global user.email annotation-extract-bot@annotation-extract-bot.local")

url = environ["url"] # ex https://archive.org/download/youtubeannotations_00/A-.tar
print(url)
itema = environ["url"].split("/")[-1].split(".")[0]

print("Downloading tar file (this may take a while)...")
urlretrieve(url, url.split("/")[-1])

print("Extracting tar file...")
tar = tarfile.open(url.split("/")[-1])

vidsl = set()
urlsl = set()
yturl = set()

# https://stackoverflow.com/a/19587581
for file in tar:
    if file:
        myfi = tar.extractfile(file)
        if myfi:
            try:
                urls = ET.parse(myfi).getroot().findall('.//url')
                for tag in urls:
                    urlint = tag.attrib['value']
                    if urlint.startswith("https://www.youtube.com/watch?"):
                        vidsl.add(urlint.split("v=")[-1].split("&")[0].split("#")[0])
                    elif urlint.startswith("https://www.youtube.com/"):
                        yturl.add(urlint.removeprefix("https://www.youtube.com/"))
                    else:
                        urlsl.add(urlint)
            except:
                print("error", file)

system("git clone "+environ["git-url"]+" repo")
urlf = open("repo/"+itema+"_urls.txt", "w")
for item in urlsl:
    urlf.write(item+"\n")
urlf.close()

vidf = open("repo/"+itema+"_vids.txt", "w")
for item in vidsl:
    vidf.write(item+"\n")
vidf.close()

yturlf = open("repo/"+itema+"_yturls.txt", "w")
for item in yturl:
    yturlf.write(item+"\n")
yturlf.close()

system("cd repo; git add .; git commit -m \"Add "+itema+"\"; git push")

applist = heroku3.from_key(environ['heroku-key']).apps(order_by="name")
currentlists = []
for app in applist:
    if app.name.startswith("annotation"):
        currentlists.append(app.config()["url"].split("/")[-1].split(".")[0])
        
desl = "A"
for item in currentlists:
    if CHARS_SAFE.index(item[0]) > CHARS_SAFE.index(desl):
        desl = item[0]

deslb = "A"
for item in currentlists:
    if CHARS_SAFE.index(item[1]) > CHARS_SAFE.index(desl):
        desl = CHARS_SAFE[CHARS_SAFE.index(item[1]) + 1]

if CHARS_SAFE.index(deslb) > 63:
    desl = CHARS_SAFE[CHARS_SAFE.index(desl) + 1]

if CHARS_SAFE.index(desl) >= 63 and CHARS_SAFE.index(deslb) > 63:
    heroku3.from_key(environ['heroku-key']).apps()[environ['heroku-app']].scale_formation_process('worker', 0)
else:
    heroku3.from_key(environ['heroku-key']).apps()[environ['heroku-app']].config()["url"] = "https://archive.org/download/youtubeannotations_"+str(CHARS_SAFE.index(desl)).zfill(2)+"/"+desl+deslb+".tar"

sleep(1)