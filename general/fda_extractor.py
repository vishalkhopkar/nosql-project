from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

start = ord('A')
end = ord('Z')

fout = open('fda_drugs.txt', 'w')
ctr = 1
for i in range (start, end + 1):
    print('Extracting for '+chr(i))
    url = 'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=browseByLetter.page&productLetter='+chr(i)+'&ai=0'
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    for tag in tags:
        if(tag.get('href').startswith('#drugName')):
            fout.write(str(ctr)+','+tag.contents[0]+'\n')
            ctr = ctr + 1
fout.close()
