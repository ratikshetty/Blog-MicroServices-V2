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


# DATABASE = 'blog.db'
DATABASE = 'articleDB.db'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

author = ''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# app.config['BASIC_AUTH_USERNAME'] = 'john'
# app.config['BASIC_AUTH_PASSWORD'] = 'matrix'

# basic_auth = BasicAuth(app)

# class check(BasicAuth):
#     def check_credentials(username, password):
#         return true

# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     conn = sqlite3.connect('blog.db')

#     c = conn.cursor()

#     c.execute("Select password from user where name = (:username) and isDeleted=0", {"username": username})

#     pswd = c.fetchone()

#     if pswd is None:
#         return False

#     pswd = str(pswd[0])
#     db_password = hashlib.md5(password.encode())
#     db_password = str(db_password.hexdigest())    
#     # pswd = pswd[0]

#     print(pswd)
#     print(db_password)


#     if pswd is not None:
#         return pswd == db_password
    


    # return username == 'john' and password == 'matrix'

# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     # return "invalid"

#     resp = Response(status=404, mimetype='application/json')


#     return resp

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         global author 
#         author= auth.username
#         return f(*args, **kwargs)
#     return decorated


@app.route('/home', methods=['GET'])
# @basic_auth.required
def home():
    return "<h1> ******Article TEST API******* </h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
    

    # r = requests.get('http://localhost/article/retrieve/1')
    # r.status_code
    # r.headers['content-type']
    # r.encoding
    # r.text
    # return r.text 

    # fg = FeedGenerator()
    # fg.id('http://lernfunk.de/media/654321')
    # fg.title('Some Testfeed')
    # fg.author( {'name':'John Doe','email':'john@example.de'} )
    # fg.link( href='http://example.com', rel='alternate' )
    # fg.logo('http://ex.com/logo.jpg')
    # fg.subtitle('This is a cool feed!')
    # fg.link( href='http://larskiesow.de/test.atom', rel='self' )
    # fg.contributor([{'name':'John Doe', 'email':'jdoe@example.com'},{'name':'John Doe', 'email':'jdoe@example.com'},{'name':'John Doe', 'email':'jdoe@example.com'}])
    # fg.language('en')

    # rssfeed  = fg.rss_str(pretty=True)

    # return rssfeed

    # blog1 = json.loads(r.text)
    # blog1 = blog1[0]
    # r = Blog(
    #     content = blog1["content"]
    # )

    # item1 = Item(
    # title = "First article",
    # link = "http://www.example.com/articles/1", 
    # description = "This is the description of the first article",
    # author = "Santiago L. Valdarrama",
    # guid = Guid("http://www.example.com/articles/1"),
    # pubDate = datetime.datetime(2014, 12, 29, 10, 00))

    # item2 = Item(
    # title = "Second article",
    # link = "http://www.example.com/articles/2", 
    # description = "This is the description of the second article",
    # author = "Ratik L. Valdarrama",
    # guid = Guid("http://www.example.com/articles/2"),
    # pubDate = datetime.datetime(2014, 12, 30, 14, 15))

    # feed = Feed(
    # title = "Sample RSS Feed",
    # link = "http://www.example.com/rss",
    # description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
    # language = "en-US",
    # lastBuildDate = datetime.datetime.now(),
    # # items = [item1, item2],
    # blogs = [r])

    # return (feed.rss())


@app.route('/new', methods=['POST'])
#@requires_auth
def new():


    result = request.json

    if 'content' in result:
        content = result['content']
    else:
        return "Error: No content field provided. Please specify an content."

    if 'title' in result:
        title = result['title']
    else:
        return "Error: No title field provided. Please specify an title."

    # if 'author' in result:
    #     author = result['author']
    # else:
    #     return "Error: No author field provided. Please specify an author."
    global author

    author = request.authorization.username

    # connection

    

    curDate = datetime.datetime.now()

    try:
        # conn = sqlite3.connect('blog.db')
        conn = sqlite3.connect('articleDB.db')

        temp_title = title.replace(" ","%20")

        print(temp_title)

        c = conn.cursor()


        c.execute("insert into article (content, title, author, url, createdDate, modifiedDate) values (:content, :title, :author, :url, :createdDate, :modifiedDate)", {'content': content, 'title': title, 'author': author, 'createdDate': str(curDate), 'modifiedDate': str(curDate), 'url': 'http://localhost/article/search/' + temp_title})
        
        conn.commit()

        # c.execute("select * from article where isDeleted= 0")

        print(title)

        conn.close()

        resp = Response(status=201, mimetype='application/json')
        resp.headers['location'] = 'http://localhost/article/search/' + title

        # response = jsonify()
        # response.status_code = 201
        # response.headers['location'] = 'http://127.0.0.1:5000/search?title='
        # response.autocorrect_location_header = False
        # return response
        
    except sqlite3.Error as e:
        resp = Response(status=409, mimetype='application/json')

    return resp


@app.route('/search/<title>', methods=['GET'])
def search(title):

    # if 'title' in request.args:
    #     title = request.args['title']
    # else:
    #     return "Error: No title field provided. Please specify Title of the article."

    if title =='':
        return "Error: No title field provided. Please specify Title of the article."

    # connection

    # conn = sqlite3.connect('blog.db')
    conn = sqlite3.connect('articleDB.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    # db = get_db()
    
    #c = db.cursor()

    # c.execute("select count(*) from article where isDeleted = 0 and title = (:title) COLLATE NOCASE", {'title': title})

    # result=c.fetchone()
    # number_of_rows=result[0]

    # if number_of_rows == 0:
    #     resp = Response(status=404, mimetype='application/json')
    #     return resp


    c.execute("select content from article where isDeleted = 0 and title = (:title) COLLATE NOCASE", {'title': title})

    result = c.fetchone()

    if result is None:
        resp = Response(status=404, mimetype='application/json')
        return resp

    c.close()
    

    return jsonify(result)

@app.route('/edit', methods=['PATCH'])
#@requires_auth
def edit():

    result = request.json

    if 'title' in result:
        title = result['title']
    else:
        return "Error: No title field provided. Please specify an title."

    if 'content' in result:
        content = result['content']
    else:
        return "Error: No content field provided. Please specify an content."

    global author

    author = request.authorization.username


    # connection

    # conn = sqlite3.connect('blog.db')
    conn = sqlite3.connect('articleDB.db')

    c = conn.cursor()

    curDate = datetime.datetime.now()

    c.execute("""UPDATE article
            set content = (:content),
            modifiedDate = (:date),
            author = (:author)
            where title = (:title)  COLLATE NOCASE""", {'content': content, 'title': title, 'date': str(curDate), "author": author})

    conn.commit()

    conn.close()

    resp = Response(status=200, mimetype='application/json')
    return resp

    # return "Article updated"


@app.route('/delete/<title>', methods=['DELETE'])
#@requires_auth
def delete(title):

    # if 'title' in request.args:
    #     title = request.args['title']
    # else:
    if title == '':
        return "Error: No title field provided. Please specify Title of the article."

    global author

    author = request.authorization.username

    # connection

    # conn = sqlite3.connect('blog.db')
    conn = sqlite3.connect('articleDB.db')

    c = conn.cursor()

    c.execute("""update article
        set isDeleted = 1
        where isDeleted = 0 and author= (:author) and title = (:title) COLLATE NOCASE""", {'title': title, 'author': author})


    conn.commit()
    conn.close()

    resp = Response(status=200, mimetype='application/json')
    return resp

    # return "Article Deleted"

@app.route('/retrieve/<num>', methods=['GET'])
def retrieve(num):

    # if 'number' in request.args:
    #     num = request.args['number']
    # else:
        # num = -1

    # connection

    # conn = sqlite3.connect('blog.db')
    conn = sqlite3.connect('articleDB.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    if num is -1:

        c.execute("SELECT content FROM article where isDeleted = 0 ORDER BY articleId DESC")

    else:
        c.execute("""
            
            SELECT content FROM article where isDeleted = 0 ORDER BY articleId DESC LIMIT (:number)
            ;""", {'number': num})

    result = jsonify(c.fetchall())

    conn.close()

    return result

@app.route('/meta/<num>', methods=['GET'])
def meta(num):

    # if 'number' in request.args:
    #     num = request.args['number']
    # else:
    #     num = -1

    # connection

    # conn = sqlite3.connect('blog.db')
    conn = sqlite3.connect('articleDB.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    if num is -1:

        c.execute("SELECT * FROM article where isDeleted = 0 ORDER BY articleId DESC")

    else:
        c.execute("""
            
            SELECT * FROM article where isDeleted = 0 ORDER BY articleId DESC LIMIT (:number)
            ;""", {'number': num})

    result = jsonify(c.fetchall())

    conn.close()

    return result

app.run()