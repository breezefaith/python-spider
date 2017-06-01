# -*-coding:utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import requests
import threading
import string
from flask.ext.pymongo import PyMongo

def getJokes(page,mongo):
    url = "http://www.qiushibaike.com/text/page/"+page
    result=""
    strId=""
    numId=-1
    text=""
    comment=""
    '''data={
    "joke_id" : "119048549",
    "joke_content" : "小时候，一听到布谷鸟叫，就知道该吃桑葚了。记得第一次吃桑葚，楼主吃的是满嘴黑……老妈看着楼主，突然笑着问：闺女，你知道布谷鸟在说什么吗？老妈见楼主一脸懵圈，哈哈一笑说：布谷鸟在说‘布谷～布谷～吃我桑葚的黑 屁 股’……楼主：…… ",
    "comment" : {
        "comment_id" : "1",
        "comment_time" : "20170520",
        "comment_content" : "funny"
    }
    }
    mongo.db.jokes.insert_one(data)'''
    jokes=mongo.db.jokes
    try:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html,"html.parser")
        #print soup.prettify()
        #print soup.head
        i = 1
        for item in soup.find_all("div",class_='article block untagged mb15'):
            a = item.find("a",class_='contentHerf')
            #将href属性中的数字提取出来，提取结果编码为unicode，需转为utf-8
            strId = re.sub("\D","",a.attrs['href']).encode('utf-8')
            #将strId转换为数字型的numId
            numId=string.atol(strId)
            text = a.text.strip()
            
            res=jokes.find_one({"joke_id":strId})
            if(res==None):
                data={
                'joke_id':strId,
                'joke_content':text,
                'comment':[]
                }
                jokes.insert_one(data)
                comment="<div>comment area</div>"
            else:
                comment="<div>comment area"
                index=0
                for it in res['comment']:
                    index=index+1
                    comment=comment+"<div>"+str(index)+"."+it['comment_content']+"</div>"+"\n"
                comment=comment+"</div>"
            formatdiv ='<form action="" method="post" class="basic-grey-jokes"><div id="'+strId+'">'+str(i) +"."+strId+"<input type='hidden' name='page_id' value='"+page+"'/>"+"<input type='hidden' name='joke_id' value='"+ strId+"'></input>" +"\n<br/>"+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+ text +"\n"+"<br/><br/></div>"+"<div class='basic-grey'>"+comment+"</div>"+'<label><span>comment:</span>'+'<textarea id="message" name="message" placeholder="Your Message to Us"></textarea></label>'+'<label><span>&nbsp;</span>'+'<input type="submit" class="button" value="Send" /></label></form>'
            #result = result+str(i)+"."+ strId +"\n<br/>"+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+ text +"\n"+"<br/><br/>"
            result = result + formatdiv
            i=i+1

        '''
        for item in soup.find_all("div",class_='content'):
            result=result+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+(str)(i)+"."+item.span.text+"<br/><br/>"
            #file.write((str)(i)+":"+item.span.text.encode("utf-8")+"\n")
            i=i+1
        #file.close()
        #return page
        '''
        return result
    except urllib2.URLError, e:
        if(hasattr(e, "code")):
            print e.code
        if(hasattr(e, "reason")):
            print e.reason
        return result
def getIndexJokes(page,mongo):
    url = "http://www.qiushibaike.com/text/page/"+page
    result=""
    strId=""
    numId=-1
    text=""
    comment=""
    jokes=mongo.db.jokes
    try:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html,"html.parser")
        #print soup.prettify()
        #print soup.head
        i = 1
        for item in soup.find_all("div",class_='article block untagged mb15'):
            a = item.find("a",class_='contentHerf')
            #将href属性中的数字提取出来，提取结果编码为unicode，需转为utf-8
            strId = re.sub("\D","",a.attrs['href']).encode('utf-8')
            #将strId转换为数字型的numId
            numId=string.atol(strId)
            text = a.text.strip()
            res=jokes.find_one({"joke_id":strId})
            if(res==None):
                data={
                'joke_id':strId,
                'joke_content':text,
                'comment':[]
                }
                jokes.insert_one(data)
                comment="<div>comment area</div>"
            else:
                comment="<div>comment area"
                index=0
                for it in res['comment']:
                    index=index+1
                    comment=comment+"<div>"+str(index)+"."+it['comment_content']+"</div>"+"\n"
                comment=comment+"</div>"
            formatdiv ='<form action="" class="basic-grey-jokes"><div id="'+strId+'">'+str(i) +"."+strId+"<input type='hidden' name='page_id' value='"+page+"'/>"+"<input type='hidden' name='joke_id' value='"+ strId+"'></input>" +"\n<br/>"+"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+ text +"\n"+"<br/><br/></div>"+"<div class='basic-grey'>"+comment+"</div></form>"
            result = result + formatdiv
            i=i+1
            if(i==5):
                break
        return result
    except urllib2.URLError, e:
        if(hasattr(e, "code")):
            print e.code
        if(hasattr(e, "reason")):
            print e.reason
        return result