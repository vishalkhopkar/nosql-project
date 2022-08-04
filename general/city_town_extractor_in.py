from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

types = ['cities', 'towns', 'villages']
limits = [8, 23, 15]
ids = [15, 55, 56]
fout = open('places_india.txt', 'w')
ctr = 1
for i in range (0, len(types)):
    type_name = types[i]
    limit = limits[i]
    id = ids[i]
    for j in range(0, limit):
        print("Extracting data for page "+str(j+1)+" of "+type_name)
        if j != 0:
            url = 'https://www.latlong.net/category/'+type_name+'-102-'+str(id)+'-'+str(j + 1)+'.html'
        else:
            url = 'https://www.latlong.net/category/'+type_name+'-102-'+str(id)+'.html'
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup('a')
        for tag in tags:
            next_td_siblings = tag.parent.next_siblings
            lat_long = []
            for elem in next_td_siblings:
                if elem.name == 'td':
                    lat_long.append(elem.contents[0])
            if(len(lat_long) >= 2):
                print(tag.contents[0], lat_long[0], lat_long[1])
                fout.write(str(ctr)+":"+lat_long[0]+":"+lat_long[1]+":"+tag.contents[0]+"\n")
                ctr += 1
fout.close()
