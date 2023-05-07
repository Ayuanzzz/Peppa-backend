HOSTNAME = 'localhost'
# HOSTNAME = 'mysqldb'
PORT = '3306'
DATABASE = 'Peppa'
USER = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USER, PASSWORD,HOSTNAME,PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI