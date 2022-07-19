import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, Date
import os

#SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
#engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
ENGINE = create_engine("sqlite:///order.db")
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    delivery_date_deadline = Column(Date)
    price_in_dollars = Column(Float)
    price_in_rubles = Column(Float)

    def __str__(self) -> str:
        return f'Id order: {self.id}, delivery date: {self.delivery_date_deadline},' \
               f' price, $: {self.price_in_dollars}, price, ₽: {self.price_in_rubles}'


def create_db():
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)


if __name__ == "__main__":
    create_db()