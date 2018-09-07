# -*- coding: utf-8 -*-
from main.urllib_ps import pagesource
from main.remove_control_characters import remove_control_characters
import config
import re
from xml.sax.saxutils import unescape
import webapp2


siteurl = 'http://www.example.com/rss.xml'
rssname = ''


def filter():
    result = pagesource(siteurl)
#    result = remove_control_characters(result)
#    result = re.aub('', '', result)
#    result = re.aub('', '', result)
#    result = re.sub('<(/|)div.*?>', '', result)
    return result


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(filter())
app = webapp2.WSGIApplication([('/' + config.subdir4rss + '/' + rssname, MainPage)], debug=True)
