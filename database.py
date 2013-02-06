import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative

engine = sqlalchemy.create_engine('sqlite:///:memory:',echo=True,convert_unicode=True)

#should only be called once globally or at module level
db_session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = sqlalchemy.ext.declarative.declarative_base()
Base.query = db_session.query_property()

def init_db():
	import models
	Base.metadata.create_all(bind=engine)
