import mysql.connector
import sys
from datetime import datetime 
from key import password, database_name
import time

class DataBase:
    def __init__(self, name):
        print (f'database {name} runnning...')
        self.db = mysql.connector.connect(
            host="localhost",
            user="user",
            password=password
        )
        
        self.name = name 
        
        self.cursor = self.db.cursor()

        # self.cursor.execute(f"DROP DATABASE IF EXISTS {self.name}")
        
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.name}")

        self.cursor.execute(f'USE {self.name}')

        # self.cursor.execute(f"DROP TABLE signals")

        # self.cursor.execute(f"DROP TABLE locations")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS signals (mac VARCHAR(255), rssi VARCHAR(255), date VARCHAR(255))")

        self.cursor.execute('CREATE TABLE IF NOT EXISTS locations (x VARCHAR(255), y VARCHAR(255), date VARCHAR(255))')
    
    def show(self):
        self.cursor.execute("SHOW DATABASES")
        for x in self.cursor:
            print(x)
    
    def show_table(self):
        self.cursor.execute("SHOW TABLES")
        for x in self.cursor:
            print(x)
    
    def insert_signal(self, mac, rssi):
        if not type(mac) == str or not type(rssi) == int:
            print('WARNING(failed signals insert): mac should be str, rssi should be int', file = sys.stderr)
            return False
        now = datetime.now()
        formatted_date = now.strftime('%Y%m%D%H%M%S')
        # sql = "INSERT INTO signals (mac, rssi, date) VALUES (%s, %s, %s)"
        # val = (mac, str(rssi), formatted_date)
        # self.cursor.execute(sql, val)
        # self.cursor.execute("INSERT INTO signals (mac, rssi, date) VALUES ('%s', '%s', '%s')"%(mac, str(rssi), formatted_date))
        # print("print get_signal")
        # res = self.get_signal(mac=mac, last = 1)
        # for x in res: print (x)
        try:
            sql = "INSERT INTO signals (mac, rssi, date) VALUES (%s, %s, %s)"
            val = (mac, str(rssi), formatted_date)
            self.cursor.execute(sql, val)
            # self.cursor.execute("INSERT INTO signals (mac, rssi, date) VALUES ('%s', '%s', '%s')"%(mac, str(rssi), formatted_date))
            # print("ALL SIGNALS: ")
            # res = self.get_all_signals()
            # for x in res: print (x)
            # debug print
            print("get_signal")
            res = self.get_signal(mac=mac)
            for x in res: print (x)
        except Exception as e:
            print("SQL ERROR", e)
        return True 
        
    def get_signal(self, mac, last = 1):
        try: 
            sql = f"SELECT * FROM signals WHERE (mac='{mac}')"
            if last > 0:
                sql += f' ORDER BY date DESC LIMIT {last}'
            self.cursor.execute(sql)
            myresult = self.cursor.fetchall()
            return myresult
        except Exception as e:
            print(e)
            return []
    
    def get_all_signals(self, last = 5):
        sql = f'SELECT * FROM signals'
        if last > 0:
            sql += f' ORDER BY date DESC LIMIT {last}'
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        return myresult

    def insert_location(self, x, y):
        if not type(x) in (int, float) or not type(y) in (int, float):
            print('WARNING(failed locations insert): x, y should be int or float', file = sys.stderr)
            return False
        now = datetime.now()
        formatted_date = now.strftime('%Y%m%D%H%M%S')
        sql = "INSERT INTO locations (x, y, date) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (str(x),str(y),formatted_date))
        return True
    
    def get_all_locations(self, last = 5):
        sql = f'SELECT * FROM locations'
        if last > 0:
            sql += f' ORDER BY date DESC LIMIT {last}'
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        return myresult
    
    def get_location(self, last = 1):
        try: 
            sql = 'SELECT * FROM locations'
            if last > 0:
                sql += f'ORDER BY date DESC LIMIT {last}'
            self.cursor.execute(sql)
            myresult = self.cursor.fetchall()
            return myresult
        except Exception as e: 
            print(e)
            return []
    def clear(self):
        # self.cursor.execute(f"DROP DATABASE IF EXISTS {self.name}")
        print("hello world")
        # time.sleep(1)
        
global_db = DataBase(database_name)

if __name__ == '__main__':
    # db = DataBase("test")
    db = global_db
    print ('----test0-----')
    db.insert_signal(mac = '12345', rssi = 20)
    db.insert_signal(mac = '345678', rssi = 30)
    db.show()
    print ('----table-----')
    db.show_table()
    print ('----test1-----')
    res = db.get_signal(mac='12345', last = 1)
    for x in res: print (x)
    print ('----test2-----')
    res = db.get_signal(mac='12312r', last = 1) # failed now 
    for x in res: print (x)
    print ('----test3-----')
    res = db.insert_location(1,2)
    res = db.insert_location(3,4)
    res = db.get_location(last = 2)
    for x in res: print (x)
    res = db.insert_location(5,6)
    print(x)
    db.show_table()