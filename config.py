from decouple import config

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'
DEBUG = True

# Database
POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'fairfrog',
    'host': 'localhost',
    'port': '5432',
}
# SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/'
#   '%(db)s' % POSTGRES

user = config('DBUSER')
pwd = config('DBPASSWD')
server = config('DBSERVER')
database = config('DB')
SQLALCHEMY_DB_URI = f'mysql+pymysql://{user}:{pwd}@{server}/{database}' + '?charset=utf8mb4'
SQLALCHEMY_POOL_RECYCLE = 270
SQLALCHEMY_ECHO = True
