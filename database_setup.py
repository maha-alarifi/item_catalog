import sys

from sqlalchemy import Column, Foreignkey, Integer, String

from sqlalchemy.ext.declarative import declarative_base()


from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()
###############################################################################
class Category(Base):
    __tablename__ = 'category' #representation of the table in the database
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

#=============================================================================#
class Item(Base):
    __tablename__ = 'item' #representation of the table in the database
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    category_id = Column(Integer, Foreignkey('category.id'))
    category = relationship(Category)

###############################################################################
engine = create_engine('sqlite:///categoriesmenu.db')
Base.metadata.create_all(engine)
