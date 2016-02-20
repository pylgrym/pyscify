# MyDB.py - to offer MyDB.conn/MyDB.cur.

import pymysql


conn = None
cur = None

def initDB():
  global conn,cur
  if conn: # != None:
    return # already initd.

  conn = pymysql.connect(host='localhost',port=3306,user='jg',passwd='fyqd1275',db='todo1')
  #cur = conn.cursor()
  cur = conn.cursor(pymysql.cursors.DictCursor)

def ensureDB():
  initDB()

def shutdownDB():
  global conn,cur
  cur.close()
  conn.commit()
  conn.close()
