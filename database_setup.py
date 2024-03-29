import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()
###############################################################################
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'neme':self.name,
            'id':self.id,
        }

#=============================================================================#
class Category(Base):
    __tablename__ = 'category' #representation of the table in the database
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'neme':self.name,
            'id':self.id,
            'user_id':self.user_id
        }

#=============================================================================#
class Item(Base):
    __tablename__ = 'item' #representation of the table in the database
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'neme':self.name,
            'description':self.description,
            'id':self.id,
            'user_id':self.user_id
        }

###############################################################################
engine = create_engine('sqlite:///categoriesmenuwithusers.db')
Base.metadata.create_all(engine)
