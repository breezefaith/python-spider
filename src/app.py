from flask import Flask, render_template, request
from flask.ext.pymongo import PyMongo
from jokeSpider import *
from newsSpider import *
from newsItem import *
import random
import time

app = Flask(__name__)
mongo = PyMongo(app)

@app.route("/")
def hello():
	newsData=getIndexNews(mongo)
	index=random.randint(1, 40)
	jokesData=getIndexJokes(str(index),mongo)
	return render_template("index.html",newsData=newsData,jokesData=jokesData)

@app.route("/video")
def video():
	return render_template("video.html")
@app.route("/select",methods=["POST"])
def select():
	video=request.form.get('videos')
	return render_template("video.html",result=video)

@app.route("/test")
def test():
	return render_template("test.html")

@app.route("/news",methods=['GET','POST'])
def news():
	if(request.method=='POST'):
		url_id=request.form.get("url_id")
		comment_id='0'
		comment_time=time.strftime('%Y%m%d',time.localtime(time.time()))
		comment_content=request.form.get('message')
		data={
		'comment_id':comment_id,
		'comment_time':comment_time,
		'comment_content':comment_content
		}
		news=mongo.db.news
		res=news.find_one({'url_id':url_id})
		res['comment'].append(data)
		news.update({"url_id":url_id},res)
		newsData=getNews(mongo)
	elif(request.method=='GET'):
		newsData=getNews(mongo)
	return render_template("news.html",newsData=newsData)

@app.route("/newsitem",methods=['GET','POST'])
def newsItem():
	if(request.method=='GET'):
		url_id=request.args.get('id')
		if(url_id==None):
			return render_template("news.html",newsData=getNews(mongo))
		newsItemData=getNewsItem(url_id,mongo)
		if(newsItemData==None):
			return render_template("404.html")
	if(request.method=="POST"):
		url_id=request.form.get('url_id')
		comment_id='0'
		comment_time=time.strftime('%Y%m%d',time.localtime(time.time()))
		comment_content=request.form.get('message')
		data={
		'comment_id':comment_id,
		'comment_time':comment_time,
		'comment_content':comment_content
		}
		news=mongo.db.news
		res=news.find_one({'url_id':url_id})
		res['comment'].append(data)
		news.update({"url_id":url_id},res)
		newsItemData=getNewsItem(url_id,mongo)
	return render_template("newsitem.html",newsItemData=newsItemData)

@app.route("/jokes",methods=['GET','POST'])
def jokes():
	index=1
	if(request.method=='POST'):
		index=request.form.get('page_id')
		joke_id=request.form.get('joke_id')
		comment_id='0'
		comment_time=time.strftime('%Y%m%d',time.localtime(time.time()))
		comment_content=request.form.get('message')
		data={
		'comment_id':comment_id,
		'comment_time':comment_time,
		'comment_content':comment_content
		}
		jokes=mongo.db.jokes
		res=jokes.find_one({"joke_id":joke_id})
		res['comment'].append(data)
		jokes.update({"joke_id":joke_id},res)

	elif(request.method=='GET'):
		index=random.randint(1, 40)
	jokesData=getJokes(str(index),mongo)
	return render_template("jokes.html",jokesData=jokesData)

if __name__ == "__main__":
	app.run(debug = False)
