import psycopg2
from sqlalchemy.orm import sessionmaker
from creating_database import Order
import pandas as pd


def add_instance(Session, instance: Order) -> None:
    with Session() as session:
        session.add(instance)
        session.commit()


def delete_instance_by_id(Session, instance_id: int, instance_type) -> None:
    with Session() as session:
        session.query(instance_type).filter(instance_type.id == instance_id).delete()
        session.commit()


def add_order(engine, currency_rate_dollar_to_russian_ruble: float, order_info: dict) -> None:
    Session = sessionmaker(bind=engine)
    order_price_in_rubles = order_info["price dollars"] * currency_rate_dollar_to_russian_ruble
    order_instance: Order = Order(
        id=order_info["order number"],
        delivery_date_deadline=order_info["delivery date"],
        price_in_dollars=order_info["price dollars"],
        price_in_rubles=order_price_in_rubles
    )

    add_instance(Session, order_instance)


def delete_order_by_id(engine, order_id:int) -> None:
    Session = sessionmaker(bind=engine)

    delete_instance_by_id(Session, order_id, Order)


def get_orders(engine) -> pd.DataFrame:
    Session = sessionmaker(bind=engine)
    with Session() as session:
        orders: list[Order] = session.query(Order)

    return pd.DataFrame(data=orders, columns=Order.)


def update_order_by_id(engine, id: int, new_instance: Order) -> None:


def main():
    pass


if __name__ == "__main__":
    main()