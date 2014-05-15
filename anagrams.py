import webapp2
import sys
import urllib2
import os
import jinja2
import re
import logging
import json
import urlparse

#importing beautifulsoup
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup

#setting up jinja2 to pick files from templates dir
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#Shorthand functions to make life easier
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class Scrape(BaseHandler):
    def get(self):
        word = self.request.get('word')
        content = urllib2.urlopen('http://wordsmith.org/anagram/anagram.cgi?anagram='+word).read()
        soup = BeautifulSoup(content)
        # logging.info(parsed)
        
        self.response.headers['Content-Type'] = 'application/json'
        anagrams = []
        stidx = -1
        enidx = -1
        gramlist = list(soup.stripped_strings)
        print gramlist
        for text in gramlist:
            if text.find('No anagrams found.')>-1:
                break
            elif text.find('Displaying all:')>-1:
                stidx = gramlist.index(text) + 1
            elif text.find('What\'s New')>-1:
                enidx = gramlist.index(text)
                break
        if stidx!=-1:
            for i in range(stidx, enidx, 1):
                anagrams.append(gramlist[i])
        
        grams = json.dumps([dict(gr=gram) for gram in anagrams])
        logging.info(grams)
        obj = {
               "grams": grams
               }
        # logging.info(obj)
        # logging.info("{ \"urls\" : " +  urls + "," + " \"anchors\" : " +  anchors + " }")
        self.response.out.write("{ \"grams\" : " +  grams + " }")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/scrape/.*', Scrape)
], debug=True)
