import sqlite3

# conn = sqlite3.connect('blog.db')

# c = conn.cursor()

# # c.execute(""" CREATE TABLE article (
# #       articleId INTEGER PRIMARY KEY AUTOINCREMENT,
# #       content text,
# #       title text UNIQUE,
# #       author text,
# #       url text,   
# #       createdDate text,
# #       modifiedDate text,
# #       isDeleted INTEGER DEFAULT 0,
# #       FOREIGN KEY (author) REFERENCES user(name)
# #       )""")

# c.execute(""" CREATE TABLE comments (
#       commentId INTEGER PRIMARY KEY AUTOINCREMENT,
#       articleId INTEGER,
#       comment text,
#       author text,
#       createdDate text,
#       isDeleted INTEGER DEFAULT 0,
#       FOREIGN KEY (articleId) REFERENCES article(articleId)
#       )""")

# # c.execute(""" CREATE TABLE user (
# #       userId INTEGER PRIMARY KEY,
# #       emailid text UNIQUE,
# #       name text UNIQUE,
# #       password text,
# #       createdDate text,
# #       modifiedDate text,
# #       isDeleted INTEGER DEFAULT 0
# #       )""")

# c.execute(""" CREATE TABLE tags (
#      articleId INTEGER,
#      tag text,
#      author text,
#      createdDate text,
#      isDeleted INTEGER DEFAULT 0,
#      FOREIGN KEY (articleId) REFERENCES article(articleId),
#      FOREIGN KEY (author) REFERENCES user(name),
#      PRIMARY KEY (articleId, tag)
#      )""")


# # c.execute("INSERT INTO article VALUES ('Test content 1', 'Test title 1','Test author 1','test Date1','test updated 1')")

# c.execute("select * from article")

# print(c.fetchall())
# conn.commit()

# conn.close()

# Users Database 

conn = sqlite3.connect('userDB.db')

c = conn.cursor()

c.execute(""" CREATE TABLE user (
      userId INTEGER PRIMARY KEY,
      emailid text UNIQUE,
      name text UNIQUE,
      password text,
      createdDate text,
      modifiedDate text,
      isDeleted INTEGER DEFAULT 0
      )""")

conn.commit()

conn.close()

# Article Database

connArticle = sqlite3.connect('articleDB.db')

c = connArticle.cursor()

c.execute(""" CREATE TABLE article (
      articleId INTEGER PRIMARY KEY AUTOINCREMENT,
      content text,
      title text UNIQUE,
      author text,
      url text,   
      createdDate text,
      modifiedDate text,
      isDeleted INTEGER DEFAULT 0
      )""")
connArticle.commit()
connArticle.close()

# Comment Database

connComments = sqlite3.connect('commentsDB.db')
c = connComments.cursor()

c.execute(""" CREATE TABLE comments (
       commentId INTEGER PRIMARY KEY AUTOINCREMENT,
       
        comment text,
        author text,
        createdDate text,
        articleTitle text,
        isDeleted INTEGER DEFAULT 0     
        )""")

connComments.commit()
connComments.close

# Tag Database

connTags = sqlite3.connect('tagsDB.db')
c = connTags.cursor()

c.execute(""" CREATE TABLE tags (
      articleTitle text,
      tag text,
      author text,
      createdDate text,
      isDeleted INTEGER DEFAULT 0,
      PRIMARY KEY (articleTitle, tag)
      )""")

connTags.commit()
connTags.close()

