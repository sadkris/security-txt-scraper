import sys
import requests
import bs4
import argparse
import urllib.parse

parser = argparse.ArgumentParser(description='Scrape Google for security.txt pages, or user input')
parser.add_argument("url", nargs="?")
args = parser.parse_args()

if args.url:
  queryString = urllib.parse.quote(args.url, safe="")
  #print(queryString)

else:
  queryString = urllib.parse.quote("inurl:.well-known/security.txt", safe="")
  #print(queryString)

request = requests.get('https://google.com/search?q='+queryString)

soup = bs4.BeautifulSoup(request.text, "html.parser")

linkHunter = soup.find_all('a')

for page in linkHunter:
  for tag in str(page).split():
    if tag[:4] == "href":
      if tag.split('"')[1][:7] == "/url?q=":
        print(tag.split('"')[1].split("/url?q=")[1].split("&amp")[0])
