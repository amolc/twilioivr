import pymysql as pm
import pandas as pd
import sqlalchemy as db
import time
import uuid
from random import randint, randrange
from datetime import timezone, datetime

sqldata={"host":"dev.zionshipping.com","user":"developer_p","passwd":",EOhaVgo5y}e","database":"zionshipping_dev"}

class SqlConn:
    def __init__(self):
        self.db=pm.connect(host=sqldata.get('host'),user=sqldata.get('user'),passwd=sqldata.get('passwd'),database=sqldata.get('database') )
        self.cursor=self.db.cursor()
        self.engine = db.create_engine('mysql+pymysql://"developer_p:,EOhaVgo5y}e@dev.zionshipping.com/zionshipping_dev')   
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.shippings = db.Table('shippings', self.metadata, autoload=True, autoload_with=self.engine)
       
    def die(self):
        self.db.close()


    def viewdata(self):
        self.sql="select * from shippings"
        self.cursor.execute(self.sql)
        self.row=self.cursor.fetchall()
        sql_data = pd.DataFrame(self.row)
        print(sql_data)
        return self.row