# -*- coding: utf-8 -*-
__author__ = 'Shinobu Jamella Hoshino, knochenflamme@gmail.com'

import urlfetch_ps
import urllib_ps
import Entdecker
from remove_control_characters import remove_control_characters
import chardet
import random
import re
import urlparse
import threading
import time
from lxml import etree
from lxml.etree import CDATA
from xml.sax.saxutils import unescape
ISOTIMEFORMAT = '%a, %e %b %Y %H:%M:%S %z'



''''''''''''''''''''''''''''''
'''从feed抓取全文，多线程 '''
''''''''''''''''''''''''''''''


def ausfuehren(lib_or_fetch, siteurl, reg4nextpage, reg4text, reg4comment, Anzahl, *custom_para):
    if lib_or_fetch == 'use_urlfetch':
        lib_or_fetch = urlfetch_ps.pagesource
    else:
        lib_or_fetch = urllib_ps.pagesource

    rss = lib_or_fetch(siteurl[0])
    if re.search(r'ERROR! QwQ', rss):
        f = open('main/Vorlage_Error.xml')
        root = etree.XML(f.read(), etree.XMLParser(remove_blank_text=True))
        f.close()
        root.xpath('/rss/channel/title')[0].text = siteurl[0]
        root.xpath('/rss/channel/link')[0].text = siteurl[0]
        root.xpath('/rss/channel/description')[0].text = siteurl[0]
        root.xpath('/rss/channel/lastBuildDate')[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))

        root.xpath('//item[1]/description')[0].text = rss
        root.xpath('//item[1]/link')[0].text = siteurl[0]
        root.xpath('//item[1]/guid')[0].text = siteurl[0]
        root.xpath('//item[1]/pubDate')[0].text = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
        return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    else:
        root = etree.XML(rss, etree.XMLParser(recover=True))
        l = len(root.xpath('//item'))

        def rssmodi(lib_or_fetch, reg4nextpage, reg4text, reg4comment, root):
            artikelurl = root.xpath('//item[$i]/link', i = Nummer)[0].text
            artikelurl = re.sub('/\?utm_source=RSS.+', '', artikelurl)
            artikelurl = re.sub('/\?ncid=rss_truncated', '', artikelurl)
            #用抓取的全文替换原description，并将正文regex中的每个分组合成一个字符串
            SeiteQuelle = lib_or_fetch(artikelurl)
            encoding = chardet.detect(SeiteQuelle)['encoding']
            #判断regex是否有效
            if len(re.findall(reg4text, SeiteQuelle)) != 0:
                #判断正文正则结果是否只有一组
                txt_tmp = re.findall(reg4text, SeiteQuelle)
                if isinstance(txt_tmp[0], tuple) is True:
                    vtext = []
                    for g in txt_tmp:
                        vtext.append("".join(g))	#移除decode('utf-8')
                else:
                    vtext = [txt_tmp[0]]	#移除decode('utf-8')

                comments = ''
                Ergebnis = Entdecker.ausfuehren(lib_or_fetch, artikelurl, SeiteQuelle, reg4nextpage, reg4text, reg4comment, vtext, comments)
                Haupttext = "".join(Ergebnis[0]).replace(r'<![CDATA\[', '').replace(r']]>', '')
#                print comments

                if len(reg4comment) == 0:
                    try:
                        root.xpath('//item[$i]/description', i = Nummer)[0].text = CDATA(Haupttext)
                    except ValueError:
                        if len(custom_para) == 1:
                            root.xpath('//item[$i]/description', i = Nummer)[0].text = CDATA(remove_control_characters(Haupttext.decode(custom_para[0])))
                        else:
                            root.xpath('//item[$i]/description', i = Nummer)[0].text = CDATA(remove_control_characters(Haupttext.decode(encoding, 'replace')))
                else:
                    try:
                        root.xpath('//item[$i]/description', i = Nummer)[0].text = CDATA(Haupttext + Ergebnis[1])
                    except ValueError:
                        if len(custom_para) == 1:
                            root.xpath('//item[$i]/description', i = Nummer)[0].text = CDATA(remove_control_characters(Haupttext.decode(custom_para[0]) + Ergebnis[1].decode(custom_para[0])))
                        else:
                            root.xpath('//item[$i]/description', i = Nummer)[0].text = CDATA(remove_control_characters(Haupttext.decode(encoding, 'replace') + Ergebnis[1].decode(encoding, 'replace')))

            elif re.search(r'ERROR! QwQ', SeiteQuelle):
                root.xpath('//item[$i]/description', i = Nummer)[0].text = '<span style="color:rgb(255,0,0);font-size:30px;">' + SeiteQuelle + '</span>'	#移除decode('utf-8') #error信息可能需要添加decode
            #regex无效
            else:
                root.xpath('//item[$i]/description', i = Nummer)[0].text = '<span style="color:rgb(255,0,0);font-size:30px;">Error: Please check regex</span>'

        #限制抓取的文章数
        if Anzahl == 0 or Anzahl >= l:
            for Nummer in random.sample(range(1, l+1), l):
                t = threading.Thread(target=rssmodi, args=(lib_or_fetch, reg4nextpage, reg4text, reg4comment, root))
                t.start()
                t.join()
                time.sleep(float(random.sample(range(1, 6), 1)[0]))
        elif Anzahl < l:
            for x in range(Anzahl+1, l+1)[::-1]:
                item = root.xpath('//item[$i]', i = x)[0]
                item.getparent().remove(item)
            for Nummer in random.sample(range(1, Anzahl+1), Anzahl):
                t = threading.Thread(target=rssmodi, args=(lib_or_fetch, reg4nextpage, reg4text, reg4comment, root))
                t.start()
                t.join()
                time.sleep(float(random.sample(range(1, 6), 1)[0]))

        #格式化以符合xml规范
        result = re.sub('<title>(?!<\!\[CDATA\[)', r'<title><![CDATA[', unescape(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')))
        result = re.sub('(?<!\]\]>)</title>', r']]></title>', result)
        result = re.sub('<description>(?!<\!\[CDATA\[)', r'<description><![CDATA[', result)
        result = re.sub('(?<!\]\]>)</description>', r']]></description>', result)
        result = re.sub('<category>(?!<\!\[CDATA\[)', r'<category><![CDATA[', result)
        result = re.sub('(?<!\]\]>)</category>', r']]></category>', result)
        return re.sub(r'(<|&#60;|&lt;)(/|)(body|html)(>|&#62;|&gt;)', '', result)

