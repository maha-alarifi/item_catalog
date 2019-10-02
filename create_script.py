from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
engine = create_engine('sqlite:///categoriesmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

b = Category(name = 'B')
session.add(b)
session.commit()

b_a = Item(name = 'B_a', description = 'first item of first category', category = b)
session.add(b_a)
session.commit()

b_b = Item(name = 'B_b', description = 'first item of first category', category = b)
session.add(b_b)
session.commit()


c = Category(name = 'C')
session.add(c)
session.commit()

c_a = Item(name = 'C_a', description = 'first item of first category', category = c)
session.add(c_a)
session.commit()

c_b = Item(name = 'C_b', description = 'first item of first category', category = c)
session.add(c_b)
session.commit()

c_c = Item(name = 'C_c', description = 'first item of first category', category = c)
session.add(c_c)
session.commit()

d = Category(name = 'D')
session.add(d)
session.commit()

d_a = Item(name = 'D_a', description = 'first item of first category', category = d)
session.add(d_a)
session.commit()

d_b = Item(name = 'D_b', description = 'first item of first category', category = d)
session.add(d_b)
session.commit()

d_c = Item(name = 'D_c', description = 'first item of first category', category = d)
session.add(d_c)
session.commit()

d_d = Item(name = 'D_d', description = 'first item of first category', category = d)
session.add(d_d)
session.commit()


e = Category(name = 'E')
session.add(e)
session.commit()

e_a = Item(name = 'E_a', description = 'first item of first category', category = e)
session.add(e_a)
session.commit()

e_b = Item(name = 'E_b', description = 'first item of first category', category = e)
session.add(e_b)
session.commit()

e_c = Item(name = 'E_c', description = 'first item of first category', category = e)
session.add(e_c)
session.commit()

e_d = Item(name = 'E_d', description = 'first item of first category', category = e)
session.add(e_d)
session.commit()

e_e = Item(name = 'E_e', description = 'first item of first category', category = e)
session.add(e_e)
session.commit()
