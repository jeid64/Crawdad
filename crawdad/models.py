from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Unicode, Text, DateTime, ForeignKey
from sqlalchemy import Column, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from datetime import datetime
import logging


logger = logging.getLogger("crawdad.models")
_Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class User(_Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uid = Column(Unicode(255))
    name = Column(Unicode(255))
    admin = Column(Boolean)
    created_at = Column(DateTime())
    messages = relationship("Message")

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            uid=self.uid,
            admin=self.admin,
            created_at=self.created_at.strftime("%D %H:%M"))


class APIKey(_Base):
    __tablename__ = "apikeys"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime())
    apikey = Column(Unicode(255))
    name = Column(Unicode(255))
    #messages = relationship("Message")

    def to_dict(self):
        return dict(
            id=self.id,
            create_at=self.create_at,
            apikey=self.apikey,
            owner_id=self.owner_id)


class Message(_Base):
    __tablename__ = "messages"
    #__mapper_args__ = dict(order_by="created_at desc")

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime())
    #printed_at = Column(DateTime())
    #print_fin_time = Column(DateTime())
    text = Column(Text())
    #apikey = Column(Integer, ForeignKey('apikeys.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            owner_id=self.owner_id,
            created_at=self.created_at.strftime("%D %H:%M"),
            #print_start_time=self.last_updated.strftime("%D %H:%M"),
            #print_fin_time=self.last_updated.strftime("%D %H:%M"),
            text=self.text
        )

    @classmethod
    def from_dict(cls, new):
        m = Message()
        m.owner_id = new.get('owner_id')
        m.created_at = datetime.now()
        #m.print_start_time = None
        #m.print_fin_time = None
        m.text = new.get('text')
        return m


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.drop_all()
    _Base.metadata.create_all(engine, checkfirst=False)

    DBSession.commit()
