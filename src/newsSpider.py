# -*-coding:utf-8 -*-
import requests
import re
import urllib2
import time
import random
import json
from bs4 import BeautifulSoup


def getContent(url):
    #url="http://news.sohu.com/20170515/n493088223.shtml"
    r=requests.get(url)
    s=r.content
    soup = BeautifulSoup(s, 'html.parser')
    str=""
    for h1 in soup.find_all('p'):
        #print(type(h1.text))
        str=str+h1.text+"\n"
    #print(str)
    return str
def getTitle(url):
    r=requests.get(url)
    s=r.content
    soup = BeautifulSoup(s, 'html.parser')
    str=""
    for h1 in soup.find_all('h1'):
        #print(type(h1.text))
        str=str+h1.text+"\n"
    #print(str)
    return str
def getLinks(url):
    
    r=requests.get(url)
    s=r.content
    links=re.findall("<span class=\"com-num\"><a target=\"_blank\" href=\"#\">comment num</a></span><a target=\"_blank\" href=\"(.*?)\">",s)
    return links

#print(s)
def getData():
    url="http://news.sohu.com/shehuixinwen.shtml"
    r=requests.get(url)
    s=r.content
    Max=re.findall("var maxPage = (.*?);",s)
    Max=int(Max[0])
    i=Max
    ret={}
    #print(Max)
    while i>Max-1:
        if i==Max:
            url="http://news.sohu.com/shehuixinwen.shtml"
        else:
            url="http://news.sohu.com/shehuixinwen_"+str(i)+".shtml"
        links=getLinks(url)
        for j in links:
     #       print(j)
            if(j.startswith("http://www")==False):
                continue
            title=getTitle(j)
            content=getContent(j)
            if len(content)==0 or len(title)==0:
                continue
            if j in ret.keys():
                continue
            #  j 表示 新闻的链接，title表示新闻的标题 ,content表示新闻的内容  判断一下 j  是不是存在数据库里  如果在 就不插入  ，不在就分别把j,title还有content 插入
            temp=[]
            temp.append(title)
            temp.append(content)
            ret[j]=temp
        i=i-1

    return ret
    #  ret是一个字典，key是url，value是[title,content]这样一个列表
    
def getNews(mongo):
    ret=getData()
    result=""
    comment=""
    #print(len(ret.keys()))
    news=mongo.db.news
    for item in ret.items():
        url,temp=item
        url_id=url[url.rfind("/")+1:len(url)]
        title=temp[0]
        content=temp[1]
        res=news.find_one({'url':url})
        if(res==None):
            data={
            'url_id':url_id,
            'url':url,
            'title':title,
            'content':content,
            'comment':[]
            }
            news.insert_one(data)
            comment="<div class='basic-grey-news-comment'><strong>comment area</strong>"
            #print "insert success"
        else:
            #print ""
            comment="<div class='basic-grey-news-comment'><strong>comment area</strong>"
            index=0
            for it in res['comment']:
                index=index+1
                comment=comment+"<div class=''>"+str(index)+"."+it['comment_content']+"</div>"+"\n"
            comment=comment+"</div>"
        formatdiv ='<form action="" method="post" class="basic-grey-news"><div>'+"<input type='hidden' name='url_id' value='"+url_id+"'/>"+"\n<br/>"+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='/newsitem?id="+url_id+"'><strong>"+ title +"</strong></a><br/><div class='basic-grey-summary'>"+content[0:100]+"\n"+"<a href='"+url+"'>[detail]</a></div></div>"+"<div class='basic-grey-news'>"+comment+"</div>"+'<label><span>comment:</span>'+'<textarea id="message" name="message" placeholder="Your Message to Us"></textarea></label>'+'<label><span>&nbsp;</span>'+'<input type="submit" class="button" value="Send" /></label>'+'</form>'
        #f.write(u"".join(formatdiv).encode("utf-8")+"\n")
        result = result + formatdiv
    return result
def getIndexNews(mongo):
    ret=getData()
    result=""
    comment=""
    #print(len(ret.keys()))
    news=mongo.db.news
    i=0
    for item in ret.items():
        url,temp=item
        url_id=url[url.rfind("/")+1:len(url)]
        title=temp[0]
        content=temp[1]
        res=news.find_one({'url':url})
        if(res==None):
            data={
            'url_id':url_id,
            'url':url,
            'title':title,
            'content':content,
            'comment':[]
            }
            news.insert_one(data)
            comment="<div class='basic-grey-news-comment'>comment area"
            #print "insert success"
        else:
            #print ""
            #comment="<div>comment area"
            comment="<div class='basic-grey-news-comment'>comment area"
            index=0
            for it in res['comment']:
                index=index+1
                comment=comment+"<div>"+str(index)+"."+it['comment_content']+"</div>"+"\n"
            comment=comment+"</div>"
        formatdiv ='<form action="" method="post" class="basic-grey-news"><div>'+"<input type='hidden' name='url_id' value='"+url_id+"'/>"+"\n<br/>"+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='/newsitem?id="+url_id+"'><strong>"+ title +"</strong></a><br/><div class='basic-grey-summary'>"+content[0:100]+"\n"+"<a href='"+url+"'>[detail]</a></div></div>"+"<div class='basic-grey-news'>"+comment+"</div>"+'</form>'
        #f.write(u"".join(formatdiv).encode("utf-8")+"\n")
        result = result + formatdiv
        i=i+1
        if(i==5):
            break
    return result