import requests
from bs4 import BeautifulSoup
response=requests.get('https://en.wikipedia.org/wiki/Ram_Mandir')
content = response.content
content = response.text
status_code = response.status_code
headers = response.headers
soup = BeautifulSoup(content,'html.parser')
print("Status Code: ", status_code)
print("\nHeaders:\n", headers)
print("\nContent:\n", content)
page_title = soup.find('title').string
print("\nPage Title: ")
print(page_title)
def extract_article(url):
    
    
   
    response = requests.get(url)                                                            
    
    soup = BeautifulSoup(response.content, "html.parser")                                   
    intro_header = soup.find(id="Introduction")                                             
    if intro_header is None:                                                                 
        return None
    else:
        
        article=""