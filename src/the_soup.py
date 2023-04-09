print("hello")
# from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
url = 'https://ksita.com'
request = Request(url)
response = urlopen(request)
response = response.read()
print(response)

# with open("index.html", "r") as f:
#     doc = BeautifulSoup(f, "html.parser")
#
# print(doc.prettify())
