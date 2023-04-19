HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'Peppa'
USER = 'root'
PASSWORD = ''
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USER, PASSWORD,HOSTNAME,PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI