import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser
from urllib import parse

url = "http://www.keei.re.kr/web_keei/d_results.nsf/0/30BD4E9B4EC031C649258205002A52F6/$file/171124_%EC%A0%9C9%EA%B8%B0%20%EC%B0%A8%EC%84%B8%EB%8C%80%EC%97%90%EB%84%88%EC%A7%80%EB%A6%AC%EB%8D%94%EA%B3%BC%EC%A0%95%2010%EC%A3%BC%EC%B0%A8%202%ED%8A%B9%EA%B0%95%20%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C.pdf"
_directory="./pdf"
last = url.split('/')[-1]
filename = parse.unquote(last.split('.')[0]) +'.pdf'
full_path = _directory + '/' + filename

print(url, full_path)
urllib.request.urlretrieve(url, full_path)