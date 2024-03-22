import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:postgres@localhost:5432/netology_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# создание объектов БД
# publishers
tolstoy = Publisher(name="Tolstoy")
dostoevsky = Publisher(name="Dostoevsky")
mitchel = Publisher(name="Mitchel")

# books
world_and_piece = Book(title="Война и мир", publisher=tolstoy)
crime = Book(title="Преступление и наказание", publisher=dostoevsky)
gone_wind = Book(title="Унесенные ветром", publisher=mitchel)

# shops
mir_knig = Shop(name="Мир книг")
azbuka = Shop(name="Азбука")

# stocks
mir_knig_stock = Stock(count=3, id_book=1, id_shop=1, book=world_and_piece, shop=mir_knig)
azbuka_stock_crime = Stock(count=5, id_book=2, id_shop=2, book=crime, shop=azbuka)
azbuka_stock_gone_wind = Stock(count=2, id_book=3, id_shop=2, book=gone_wind, shop=azbuka)

# sales
sale1 = Sale(price=300, date_sale='2024, 1, 14', count=1, id_stock=1, stock=mir_knig_stock)
sale2 = Sale(price=400, date_sale='2024, 2, 24', count=1, id_stock=2, stock=azbuka_stock_crime)
sale3 = Sale(price=500, date_sale='2024, 3, 5', count=1, id_stock=3, stock=azbuka_stock_gone_wind)

session.add_all(
    [tolstoy, dostoevsky, mitchel, world_and_piece, crime, gone_wind, mir_knig, azbuka, mir_knig_stock,
     azbuka_stock_crime,
     azbuka_stock_gone_wind, sale1, sale2, sale3])

session.commit()

pub = input('Введите издателя: ')

query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
query = query.join(Publisher).filter(Publisher.name == pub)
query = query.join(Stock)
query = query.join(Shop)
query = query.join(Sale)
records = query.all()

for r in records:
    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
session.close()
