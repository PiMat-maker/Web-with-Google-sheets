import pandas as pd

from central_bank_api.currency_rate import convert_dollar_to_russian_ruble
from database.creating_database import create_db, ENGINE
from database.ddl_functions import add_order, get_orders, delete_order_by_id
from database.utils import convert_dataframe_row_to_dict
from google_sheets.data_uploader import upload_sheets_data
from time import sleep

TIME_BETWEEN_REQUESTS_TO_SHEETS_IN_SECONDS = 10


def main():
    #create_db()
    currency_rate_dollar_to_russian_ruble: float = convert_dollar_to_russian_ruble()
    current_database_instances: pd.DataFrame = get_orders(ENGINE).drop(["price_in_rubles"], axis=1)

    while True:
        raw_sheets_data = upload_sheets_data().rename(columns={"Order": "id", "Price, $": "price_in_dollars",
                                                               "Delivery date": "delivery_date_deadline"}).dropna()
        raw_sheets_data["delivery_date_deadline"] = pd.to_datetime(raw_sheets_data["delivery_date_deadline"],
                                                                   format="%d.%m.%Y").apply(lambda x: x.date())
        sheets_data = raw_sheets_data.astype(
            {"id": int, "price_in_dollars": float})

        difference_between_data_versions = sheets_data.merge(current_database_instances, how='outer',
                                                             on=['id', 'price_in_dollars',
                                                                 'delivery_date_deadline'],
                                                             suffixes=('', '_new'), indicator=True)

        difference_between_data_versions = difference_between_data_versions \
            .loc[difference_between_data_versions["_merge"] != "right_only"]

        keys = sheets_data.keys()
        for i in range(difference_between_data_versions.shape[0]):
            current_row = difference_between_data_versions.iloc[i]
            if current_row["_merge"] == "left_only":
                order = convert_dataframe_row_to_dict(current_row, keys)
                delete_order_by_id(ENGINE, current_row["id"])
                add_order(ENGINE, currency_rate_dollar_to_russian_ruble, order)

        current_database_instances = difference_between_data_versions.drop(["_merge"], axis=1)

        sleep(TIME_BETWEEN_REQUESTS_TO_SHEETS_IN_SECONDS)
        print("Cycle")


if __name__ == "__main__":
    main()
