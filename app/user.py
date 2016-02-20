
#User.py
import pymysql

import MyDB

#class Rec:
#    def __init__(self, **entries): 
#        self.__dict__.update(entries)






"""
create table users (
  userId int           not null auto_increment, 
  email varchar(128)   not null, 
  password varchar(40) not null,

   PRIMARY KEY     (userId)
);

create table users (
  userId number, -- can I control/name this/avoid this?
  email varchar2(128), -- acceptable length?
  password varchar2(40)
);

I need CRUD - create a user, delete a user,
query/find a (single)user, and update (pwd) a user.

hopefully I don't need "list many users".
"""

class User:
  def __init__(self,email=None,password=None): # not userId,
    self.userId = None # must come from db.
    self.email = email
    self.password= password

  # Not possible in python - use class factory methods instead!
  #def __init__(self): 
  #  self.userId = '' 
  #  self.email = ''
  #  self.password = ''

  def dbInsert2(self):
    MyDB.ensureDB()
    sql = ( 
     "insert into users (userId,email,password)"
     " values( %(userId)s, %(email)s, %(password)s )"
    )
    MyDB.cur.execute(sql,
      {'userId': self.userId, 'email': self.email, 'password': self.password}
    )
    MyDB.conn.commit()
    return

  def dbInsert(self):
    MyDB.ensureDB()
    sql = ( 
     "insert into users (email,password)"
     " values( %(email)s, %(password)s )"
    )
    MyDB.cur.execute(sql,
      { 'email': self.email, 'password': self.password}
    )
    self.userId = MyDB.cur.lastrowid
    #print('lastRowId:',self.userId)
    MyDB.conn.commit()
    return self.userId

  def dbUpdate(self):
    MyDB.ensureDB()
    assert(self.userId)
    sql = ("update users set"
    " email = %(email)s, password = %(password)s "
    " where userId = %(userId)s"
    )
    MyDB.cur.execute(sql,
      {'userId': self.userId, 'email': self.email, 'password': self.password}
    )
    MyDB.conn.commit()
    return

  def dbDelete(self):
    MyDB.ensureDB()
    assert(self.userId)
    sql = "delete from users where userId = %(userId)s"
    MyDB.cur.execute(sql, {'userId': self.userId } )
    MyDB.conn.commit()
    return

  @classmethod
  def dbFindById(cls, userId): #self):
    MyDB.ensureDB()
    assert(userId) #self.userId)
    sql = "select userId, email,password from Users where userId = %(userId)s"
    MyDB.cur.execute(sql, {'userId': userId } )
    for r in MyDB.cur:
      user=User()
      user.__dict__.update(r)
      print('found!')
      return user
      #self.__dict__.update(r)
      #s = Rec(**r) # This is slow but neat..
      #print (s.userId, s.email, s.password)

    print('not found!')
    return None # Not found!

  @classmethod
  def dbFindByEmail(cls, email): #self):
    MyDB.ensureDB()
    print('email:', email)
    assert(email) #self.userId)
    sql = "select userId, email,password from Users where email = %(email)s"
    MyDB.cur.execute(sql, {'email': email } )
    for r in MyDB.cur:
      user=User()
      user.__dict__.update(r)
      print('found!')
      return user
      #self.__dict__.update(r)
      #s = Rec(**r) # This is slow but neat..
      #print (s.userId, s.email, s.password)

    print('not found!')
    return None # Not found!


def testUser():
  user=User("jg@here.com", "alea")
  user.dbInsert()
  user.dbUpdate()
  user3 = User.dbFind(53) #49) #2)
  user.dbDelete()
  user2=User("pallejg@here.com", "alea")
  user.dbInsert()




