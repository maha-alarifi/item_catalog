from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
engine = create_engine('sqlite:///categoriesmenuwithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Alpha", email="maha.saud.alarifi@gmail.com",
             picture='https://lh3.googleusercontent.com/-H8nIxKPB_JY/Vzmo9mOob3I/AAAAAAAAAs4/sXiwj-zLLcobI9FU8536l3WH8NmBzt0GQCEwYBhgL/w140-h133-p/0bc634da-d5c4-4c0d-96ee-61b2043cf8ad')
session.add(User1)
session.commit()


User2 = User(name="Beta", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()


b = Category(name = 'B', user_id=1)
session.add(b)
session.commit()

b_a = Item(name = 'B_a', description = 'first item of first category', category = b, user_id=1)
session.add(b_a)
session.commit()

b_b = Item(name = 'B_b', description = 'first item of first category', category = b, user_id=1)
session.add(b_b)
session.commit()


c = Category(name = 'C', user_id=2)
session.add(c)
session.commit()

c_a = Item(name = 'C_a', description = 'first item of first category', category = c, user_id=2)
session.add(c_a)
session.commit()

c_b = Item(name = 'C_b', description = 'first item of first category', category = c, user_id=2)
session.add(c_b)
session.commit()

c_c = Item(name = 'C_c', description = 'first item of first category', category = c, user_id=2)
session.add(c_c)
session.commit()

d = Category(name = 'D', user_id=2)
session.add(d)
session.commit()

d_a = Item(name = 'D_a', description = 'first item of first category', category = d, user_id=2)
session.add(d_a)
session.commit()

d_b = Item(name = 'D_b', description = 'first item of first category', category = d, user_id=2)
session.add(d_b)
session.commit()

d_c = Item(name = 'D_c', description = 'first item of first category', category = d, user_id=2)
session.add(d_c)
session.commit()

d_d = Item(name = 'D_d', description = 'first item of first category', category = d, user_id=2)
session.add(d_d)
session.commit()


e = Category(name = 'E', user_id=1)
session.add(e)
session.commit()

e_a = Item(name = 'E_a', description = 'first item of first category', category = e, user_id=1)
session.add(e_a)
session.commit()

e_b = Item(name = 'E_b', description = 'first item of first category', category = e, user_id=1)
session.add(e_b)
session.commit()

e_c = Item(name = 'E_c', description = 'first item of first category', category = e, user_id=1)
session.add(e_c)
session.commit()

e_d = Item(name = 'E_d', description = 'first item of first category', category = e, user_id=1)
session.add(e_d)
session.commit()

e_e = Item(name = 'E_e', description = 'first item of first category', category = e, user_id=1)
session.add(e_e)
session.commit()
