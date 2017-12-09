gpipe43 is a full text RSS generator which can hosted on Google App Engine. Use Regex to search and format full text from a article, or any other content that you want.<br>
Inspired by Yahoo Pipes and Feed43.<br>
Yahoo Pipe RIP.

Feature
===
* Support multi page.
* Display all images of article's gallery.
* Appending article's comment is possible.

Prepare
====
* [Create a new Cloud Platform project and App Engine application](https://cloud.google.com/appengine/docs/standard/python/quickstart)
* [Create a bucket in google cloud storage](https://cloud.google.com/storage/docs/quickstart-console)

Simple quickstart
====
### Edit /main/user_agents.py
* add UA
### Edit config.py
* `prjname`: Name of your project on app engine
* `bucket_name`: Name of bucket
* `subdir4bg`: The crawler working under http://[prjname].appspot.com/[subdir4bg]/[rssname]
* `subdir4rss`: This is your RSS site: http://[prjname].appspot.com/[subdir4rss]/[rssname]
### Edit example.py，replace 'example' to your own RSS's name
* `rssname`: Your own RSS's name
* `siteurl`: The website that you want to generat RSS
* `reg4site`: Regex that can find articles' URL<br><br>
* `reg4title`: Regex for title in a article
* `reg4pubdate`: Regex for publish date in a article
* `reg4text`: Regex for text
* `reg4comment`: Regex for comment. Not necessary, can leave it blank. You can also use this Regex to find all the image of a gallery in the text.
* `reg4nextpage`: Regex for arctile's next page, can leave it blank.
* `Anzahl`: How much article will be generated. 0 = no limit<br><br>
* `rssgen.ausfuehren('use_urllib/use_urlfetch', 'st/mt', siteurl, reg4site, reg4title, reg4pubdate, reg4text, reg4comment, reg4nextpage, Anzahl)`: Generat a RSS for a website
* `feed_fulltext.ausfuehren('use_urllib/use_urlfetch', siteurl, reg4nextpage, reg4text, reg4comment, Anzahl, rssname)`: Use this to generat fulltext for a RSS feed.
	* `use_urllib`: Use urllib2，with UA
	* `use_urlfetch`: Use urlfetch，no UA
	* `mt`: Multi threading
	* `st`: Single threading


### Edit feed_list.py
* Replace 'example' to your own RSS's name

### app.yaml, cron.yaml
* Replace subdir4bg, subdir4rss, example to your own.<br>
See official guide: [app.yaml Reference](https://cloud.google.com/appengine/docs/standard/python/config/appref), [Scheduling Tasks With Cron for Python](https://cloud.google.com/appengine/docs/standard/python/config/cron)

### Optional
* Edit ./main/Vorlage.xml and Vorlage_Error.xml, you can the properties of elements 'generator', 'webMaster' and 'copyright' to your own.

Upload to app engine
====
* cd to the directory of your project
>gcloud config set project PROJECT_NAME<br>
>gcloud app deploy app.yaml cron.yaml --version=VERSION_NUMBER<br>

See official guide: [Deploying a Python App](https://cloud.google.com/appengine/docs/standard/python/tools/uploadinganapp)

