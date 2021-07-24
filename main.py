# Based on https://stackoverflow.com/questions/29266605, https://stackoverflow.com/questions/38309395/

print("Initializing...")

from os import system, environ, walk
from os.path import join
import heroku3
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET

url = environ["url"] # ex https://archive.org/download/youtubeannotations_00/A-.tar
item = environ["url"].split("/")[-1].split(".")[0]

print("Downloading tar file (this may take a while)...")
urlretrieve(url, url.split("/")[-1])

print("Extracting tar file...")
system("tar -x -f "+ url.split("/")[-1] + "data")

vidsl = set()
urlsl = set()

# https://stackoverflow.com/a/19587581/9811991
for subdir, dirs, files in walk("data"):
    for file in files:
        urls = ET.parse(join(subdir, file)).getroot().findall('.//url')
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

system("cd repo; git commit -m \"Add "+item+"\"; git push")
heroku3.from_key(environ['heroku-key']).apps()[environ['heroku-app']].scale_formation_process('worker', 0)
