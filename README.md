gpipe43 is a full text RSS generator which can hosted on gae. Support article that contain more than 1 page.

Prepare
====
* [Create a new Cloud Platform project and App Engine application](https://cloud.google.com/appengine/docs/standard/python/quickstart)
* [Create a bucket in google cloud storage](https://cloud.google.com/storage/docs/quickstart-console)

Simple quickstart
====
### Edit /main/user_agents
* add UA
### Edit config.py
* __prjname__: Name of your project on app engine
* __bucket_name__: Name of bucket
* __subdir4bg__: The crawler working under http://prjname.appspot.com/subdir4bg/rssname
* __subdir4rss__: This is your RSS site: http://prjname.appspot.com/subdir4rss/rssname
### Edit example.py，replace 'example' to your own RSS's name
* __rssname__: Your own RSS's name
* __siteurl__: The website that you want to generat RSS
* __reg4site__: Regex that can find articles' URL<br><br>
* __reg4title__: Regex for title in a article
* __reg4pubdate__: Regex for publish date in a article
* __reg4text__: Regex for text
* __reg4comment__: Regex for comment. Not necessary, can leave it blank. You can also use this Regex to find all the image of a gallery in the text.
* __reg4nextpage__: Regex for arctile's next page, can leave it blank.
* __Anzahl__: How much article will be generated. 0 = no limit<br><br>
* __rssgen.ausfuehren('use_urllib/use_urlfetch', 'st/mt', siteurl, reg4site, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage, Anzahl)__: Generat a RSS for a website
* __feed_fulltext.ausfuehren('use_urllib/use_urlfetch', siteurl, reg4nextpage, reg4text, reg4comment, Anzahl, rssname)__: Use this to generat fulltext for a RSS feed.
	* __use_urllib__: Use urllib2，with UA
	* __use_urlfetch__: Use urlfetch，no UA
	* __mt__: Multi threading
	* __st__: Single threading


### Edit feed_list.py
* Replace 'example' to your own RSS's name

### app.yaml, cron.yaml
* Replace subdir4bg, subdir4rss, example to your own.<br>
See official guide: [app.yaml Reference](https://cloud.google.com/appengine/docs/standard/python/config/appref), [Scheduling Tasks With Cron for Python](https://cloud.google.com/appengine/docs/standard/python/config/cron)

Upload to app engine
====
* cd to the directory of your project
>gcloud config set project PROJECT_NAME<br>
>gcloud app deploy app.yaml cron.yaml --version=VERSION_NUMBER<br>

See official guide: [Deploying a Python App](https://cloud.google.com/appengine/docs/standard/python/tools/uploadinganapp)

