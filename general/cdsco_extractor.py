from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://cdscoonline.gov.in/CDSCO/soam/drug_data.jsp'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup('td')
fout = open('cdsco_drugs.txt', 'w')
ctr = 1
for tag in tags:
    if(tag.get("bordercolor") == '1'):
        fout.write(str(ctr)+","+tag.contents[0]+"\n")
        ctr = ctr + 1

fout.close()
