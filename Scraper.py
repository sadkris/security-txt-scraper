import sys
import requests
import bs4
import argparse
import urllib.parse

parser = argparse.ArgumentParser(description='Scrape Google for security.txt pages, or user input')
parser.add_argument("url", nargs="?")
parser.add_argument("-np", nargs="?")
args = parser.parse_args()

num_pages = 1

if args.np:
  num_pages = int(args.np)

if args.url:
  queryString = urllib.parse.quote(args.url, safe="")
  #print(queryString)

else:
  queryString = urllib.parse.quote("inurl:.well-known/security.txt", safe="")
  #print(queryString)

for page in range(1, num_pages + 1):
  request = requests.get('https://google.com/search?q='+queryString+'&start='+str((page * 10) -10))

  soup = bs4.BeautifulSoup(request.text, "html.parser")

  linkHunter = soup.find_all('a')

  for page in linkHunter:
    for tag in str(page).split():
      if tag[:4] == "href":
        if tag.split('"')[1][:7] == "/url?q=":
          # Don't print if it's a link from google
          if tag.split('"')[1].split("/url?q=")[1][8:].split('.')[1] == "google":
            continue
          # Print everything past "https://"
          if tag.split('"')[1].split("/url?q=")[1].startswith('https://'):
            print(tag.split('"')[1].split("/url?q=")[1].split("&amp")[0][8:].split('/')[0])
          # Print everything past "http://"
          elif tag.split('"')[1].split(".url?q=")[1].startswith('http://'):
            print(tag.split('"')[1].split("/url?q=")[1].split("&amp")[0][7:].split('/')[0])
          # Just print everything if it doesn't contain either "http://" or "https://"
          else:
            print(tag.split('"')[1].split("/url?q=")[1].split("&amp")[0].split('/')[0])
