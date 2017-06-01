# -*-coding:utf-8 -*-
import requests
import re
import urllib2
import time
import random
import json
from bs4 import BeautifulSoup

def getNewsItem(url_id,mongo):
	item_result=""
	item_comment=""
	news=mongo.db.news
	queryRes=news.find_one({'url_id':url_id})
	if(queryRes==None):
		return None
	else:
		item_url=queryRes['url']
		item_title=queryRes['title']
		item_content=queryRes['content']
		item_comment=item_comment+"<div>comment area"
		item_index=0
		for item in queryRes['comment']:
			item_index=item_index+1
			item_comment=item_comment+"<div>"+str(item_index)+"."+item['comment_content']+"</div>"+"\n"
    	item_comment=item_comment+"</div>"
    	item_result="<form action='' method='post' class='basic-grey-newsitem'><div>"+"<input type='hidden' name='url_id' value='"+url_id+"'/>"+"\n<br/>"+"<h2>"+ item_title +"</h2><br/><div class='basic-grey-content'>"+item_content+"\n"+"</div></div>"+"<div class='basic-grey'>"+item_comment+"</div>"+'<label><span>comment:</span>'+'<textarea id="message" name="message" placeholder="Your Message to Us"></textarea></label>'+'<label><span>&nbsp;</span>'+'<input type="submit" class="button" value="Send" /></label></form>'
    	return item_result