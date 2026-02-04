#!/usr/bin/python3
"""
Creates an RSS feed from DBLP JSON data. 
Meant to be used as CGI script but can also be used as command-line.
Feedback and pull request welcome.
Martin Monperrus
March 2016
Licence: public domain
URL: https://gist.github.com/monperrus/978079d39c1cc7b4cbae78ddd1b8ed99
Operation: https://www.monperrus.net/martin/dblp-rss.py?search=venue:FASE:
"""

import feedgenerator
import re
import os
import cgi
import re
import json
import sys
import codecs
import io
import sys
import requests
import cgitb
cgitb.enable()

query_data = cgi.FieldStorage()

searchexp = "repair"
if "search" in query_data:
  searchexp = query_data['search'].value.replace(' ','%20')

# print searchexp

# https://dblp.org/search/publ/api/?q=&h=1000&c=0&f=0&format=json&rd=1a
url = "https://dblp.org/search/publ/api/?q="+searchexp+"&h=1000&c=0&f=0&format=json&rd=1a"

response = requests.get(url)

if response.status_code != 200:
   print("Content-type: text/html")
   print()
   print('DBLP API is dead (Internal server error). Please retry later.')
   sys.exit()

print("Content-type: application/rss+xml")
print("x-url: "+url)
#print("Content-type: text/plain")
print()




#reload(sys)
#sys.setdefaultencoding('utf-8')
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)





doc = response.text
title="DBLP results on "+searchexp

feed = feedgenerator.Rss201rev2Feed(title=title,
        link=url,
        description=title,
        language="en")

#print(doc)
if "hit" in json.loads(doc)["result"]["hits"]:
  ls = json.loads(doc)["result"]["hits"]["hit"]
  # sorted is now handled by API parameter rd=1a
  #ls = sorted(,key=(lambda x: x["info"]["year"]), reverse=True)

  for i in ls:
      title=i["info"]["title"]

      # required
      if "authors" not in i["info"]: i["info"]["authors"]={"author":[]}
      #if type(i["info"]["authors"]["author"])==unicode: i["info"]["authors"]["author"]=[i["info"]["authors"]["author"]]

      feed.add_item(
        title=title,
        link=i["info"]["url"],
        description=title+" | "+", ".join(i["info"]["authors"]["author"])+" | "\
+(i["info"]["venue"] if 'venue' in i["info"] else "")\
+" | "+i["info"]["year"] if type(i["info"]["year"])=='unicode' else '',
        unique_id=i["info"]["url"]
      )

print((feed.writeString('utf-8')))
                 
  
