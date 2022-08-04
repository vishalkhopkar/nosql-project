from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

country_suffix = ''
no_of_pharmacies = 0

country_code = input('Which country\'s random data do you want? Enter 1 for US, 2 for IN\n')
if country_code == '1':
    country_suffix = 'US'
    no_of_pharmacies = 60000
else:
    country_suffix = 'IN'
    no_of_pharmacies = 800000

url = 'https://3geonames.org/randomland.'+country_suffix
print(url)
file_name = 'pharmacies_'+country_suffix+'.txt'
fout = open(file_name, 'w')
for i in range (0, no_of_pharmacies):
    print("Getting details for pharmacy #"+str(i+1))
    req = urllib.request.Request(url)
    for key in hdr:
        req.add_header(key, hdr[key])

    content = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(content, 'html.parser')
    tags = soup('strong')
    fout.write(str(i + 1)+","+tags[0].contents[0].strip()+","+tags[1].contents[0].strip()+'\n')
fout.close()
