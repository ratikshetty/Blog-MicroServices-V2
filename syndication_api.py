import flask
from flask import request, jsonify, json, Response, g, make_response
import datetime
import sqlite3
from functools import wraps
#from flask_basicauth import BasicAuth
import hashlib

from feedgen.feed import FeedGenerator
import requests
from rfeed import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/summary', methods=['GET'])
# @basic_auth.required
def home():
    # return "<h1> ******Article TEST API******* </h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
    

    r = requests.get('http://localhost/article/meta/100')

    blog1 = json.loads(r.text)

    length = len(blog1)

    a = [None] * length

    for x in range(length):

        blog_temp = blog1[x]
        r = Item(
            # content = blog_temp["content"],
            title = blog_temp["title"],
            author = blog_temp["author"],
            date = blog_temp["createdDate"],
            link = blog_temp["url"]
        )

        a[x] = r

    

    feed = Feed(
    title = "Recent Articles RSS Feed",
    link = "http://localhost/syndication/home",
    description = "This is the RSS feed to fetch most recent Articles",
    # language = "en-US",
    # lastBuildDate = datetime.datetime.now(),
    # items = [item1, item2],
    items = a)

    return (feed.rss())


@app.route('/feed', methods=['GET'])
# @basic_auth.required
def feed():
    # return "<h1> ******Article TEST API******* </h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
    
    
    
    r = requests.get('http://localhost/article/meta/100')

    items = []

    if r is not None:
        r = r.json()


    for article in r:

        # return article['title']   

        comment_tags = requests.get("http://localhost/tags/searchTag/"+ str(article['title'].replace(" ","%20")))

        

        if comment_tags is not None and comment_tags.text != '':
            comment_tags = comment_tags.json()

        tags = []
        for tag in comment_tags:
            if 'tag' in tag:
                tags.append(tag['tag'])

        comment_count = requests.get("http://localhost/comments/count/"+ str(article['title'].replace(" ","%20"))).text

        if comment_count == '':
            comment_count = "Number of comments for given article: 0"

    
        items.append(Item(
            title = article['title'],
            description =comment_count,
            categories = tags
        ))

    

        
    feed = Feed(
        title = "RSS Feed",
        link = "http://www.example.com/rss",
        description = "Full RSS FEED containing Article, tags and comment count",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = items)
    
    return feed.rss()


        

        

@app.route('/comments', methods=['GET'])
# @basic_auth.required
def comment():

    articles = requests.get('http://localhost/article/meta/100')

    items = []

    if articles is not None:
        articles = articles.json()

    for article in articles:

        article_comments = requests.get("http://localhost/comments/retrieve/"+ str(article['title'].replace(" ","%20")) + "/100")

        if article_comments is not None and article_comments.text != '':
            article_comments = article_comments.json()

        comments = []

        for comment in article_comments:
            comments.append(comment['comment'])


        items.append(Item(
                title = article['title'],
                description =article['content'],
                comment = comments
            ))

    

        
    feed = Feed(
        title = "RSS Feed",
        link = "http://www.example.com/rss",
        description = "This is a comment feed",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = items)
    
    return feed.rss()

        
    

app.run()