# -*- coding: utf-8 -*-
from main import feed_fulltext, rssgen
import config
import re
import webapp2
import cloudstorage as gcs


''''''''''''''''''
'''config start'''
''''''''''''''''''

rssname = ''
siteurl = ['http://www.example.com/']
reg4site = ''
reg4title = ''	
reg4pubdate = ''
reg4text = ''
reg4comment = ''
reg4nextpage = ''
Anzahl = 10


def filter():
    result = rssgen.ausfuehren('use_urllib', 'mt', siteurl, reg4site, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage, Anzahl)
#    result = feed_fulltext.ausfuehren('use_urllib/use_urlfetch', siteurl, reg4nextpage, reg4text, reg4comment, Anzahl)
    #format output if you want
#    result = re.aub('', '', result)
#    result = re.aub('', '', result)
    return result

''''''''''''''''''
''' config end '''
''''''''''''''''''

bucket = config.bucket_name
filename = '/' + bucket + '/' + rssname + '.xml'
class FeedSaver(webapp2.RequestHandler):
    bucket = config.bucket_name
    filename = '/' + bucket + '/' + rssname + '.xml'
    def create_file(self, filename):
        gcs_file = gcs.open(filename, 'w', content_type='text/plain')
        gcs_file.write(filter())
        gcs_file.close()
    def get(self):
        self.create_file(filename)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('<p>RSS is sucessfully generated!</p><p>Click <a href="%s">HERE</a></p>' % ('http://' + config.prjname + '.appspot.com/' + config.subdir4rss + '/' + rssname))
app = webapp2.WSGIApplication([('/' + config.subdir4bg + '/' + rssname, FeedSaver)], debug=True)
