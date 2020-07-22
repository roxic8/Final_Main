from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
db = SQLAlchemy()
engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/espa', pool_recycle=3600)
# engine = create_engine('mysql+pymysql://root:asscat123@192.168.88.104:3306/enrollment', pool_recycle=3600)