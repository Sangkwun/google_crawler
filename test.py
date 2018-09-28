import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser

text = '검색어 filetype:pdf'
text = urllib.parse.quote_plus(text)

url = 'https://google.com/search?q=' + text

response = requests.get(url)

#with open('output.html', 'wb') as f:
#    f.write(response.content)
#webbrowser.open('output.html')

soup = BeautifulSoup(response.text, 'html.parser')
for g in soup.find_all(class_='g'):
    print(g.text)
    print('-----')