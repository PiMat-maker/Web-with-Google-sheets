import psycopg2
from sqlalchemy.orm import sessionmaker
from database.creating_database import Order
import pandas as pd
from datetime import datetime


def add_instance(Session, instance: Order) -> None:
    with Session() as session:
        session.add(instance)
        session.commit()


def delete_instance_by_id(Session, instance_id: int, instance_type) -> None:
    with Session() as session:
        instance = session.query(instance_type).filter(instance_type.id == int(instance_id)).first()

        if instance:
            session.delete(instance)

        session.commit()


def add_order(engine, currency_rate_dollar_to_russian_ruble: float, order_info: dict) -> None:
    Session = sessionmaker(bind=engine)
    order_price_in_rubles = round(float(order_info["price_in_dollars"]) * currency_rate_dollar_to_russian_ruble, 2)
    order_instance: Order = Order(
        id=int(order_info["id"]),
        delivery_date_deadline=order_info["delivery_date_deadline"],
        price_in_dollars=float(order_info["price_in_dollars"]),
        price_in_rubles=order_price_in_rubles
    )

    add_instance(Session, order_instance)


def delete_order_by_id(engine, order_id: int) -> None:
    Session = sessionmaker(bind=engine)

    delete_instance_by_id(Session, order_id, Order)


def get_orders(engine) -> pd.DataFrame:
    Session = sessionmaker(bind=engine)
    with Session() as session:
        orders: list[Order] = session.query(Order).all()

    orders_in_dict = [order.__dict__ for order in orders]
    print(orders_in_dict)

    if len(orders) > 0:
        orders_df = pd.DataFrame(orders_in_dict).drop(["_sa_instance_state"], axis=1)
        return orders_df

    return pd.DataFrame(columns=["id", "delivery_date_deadline", "price_in_dollars", "price_in_rubles"])


def main():
    pass


if __name__ == "__main__":
    main()
