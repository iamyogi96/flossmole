import sys
import sqlalchemy
from sqlalchemy import *

#database setup

class dbConnect():

  def __init__(self,user,pas,adr):
    self.username = user
    self.password = pas
    self.address = adr
    try:
      self.mysql_db = create_engine('mysql://'+self.username+':'+self.password+'@'+self.address+'?charset=utf8&use_unicode=0')
      self.connection = self.mysql_db.connect()
      self.meta = MetaData()
      self.meta.bind = self.connection
    except Exception as ex:
      print ex
      sys.exit(1)

  def getTable(self,tableName):
    return Table(tableName, self.meta, autoload=True)
