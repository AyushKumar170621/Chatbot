import requests
from bs4 import BeautifulSoup
import urllib.request 

url="https://en.wikipedia.org/wiki/Mukesh_Ambani"

html = urllib.request.urlopen(url)
  
# parsing the html file
htmlParse = BeautifulSoup(html, 'html.parser')
print(htmlParse.find_all("p")[1].get_text())
#  getting all the paragraphs
# for para in htmlParse.find_all("p"):
#     if para != None:
#         print(para.get_text())