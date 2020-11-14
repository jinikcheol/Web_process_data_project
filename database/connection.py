import pymysql

def get_connection():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='data12345', db='projectdata', charset='utf8')
    return conn