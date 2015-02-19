import re
import requests

try:
    data = requests.get("https://www.facebook.com/gbntelevisionnews")
#except  as e:
#    raise MyException("There was an error: %r" % e)

page = data.text
links = re.findall("(https:\/\/www.facebook.com\/photo.php\?v\=(\d+))",data.text)
if links.count > 1:
    distinctLinks = list(set(links))
    for x in range(0,len(distinctLinks)):
        print (distinctLinks[x])
    print("Total:",len(distinctLinks))