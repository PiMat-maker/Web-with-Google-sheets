import requests
from datetime import datetime
import xmltodict

VALUTES_XML_METADATA_FIELD_NAME = "ValCurs"
VALUTES_CURRENCIES_FIELD_NAME = "Valute"
VALUTE_CODE_FIELD_NAME = "CharCode"
VALUTE_CURRENCY_FIELD_NAME = "Value"
VALUTE_NOMINAL_FIELD_NAME = "Nominal"


def get_valutes_currencies():
    current_date = datetime.now().date()
    response = requests.get(
        f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={current_date.day:02d}/{current_date.month:02d}/{current_date.year}')
    dict_data = xmltodict.parse(response.content)
    return dict_data[VALUTES_XML_METADATA_FIELD_NAME][VALUTES_CURRENCIES_FIELD_NAME]


def get_valute_currency_rate(valute_code: str, valutes_currencies: list[dict]) -> float:
    for valute_currency in valutes_currencies:
        if valute_currency[VALUTE_CODE_FIELD_NAME] == valute_code:
            raw_currency_rate: str = valute_currency[VALUTE_CURRENCY_FIELD_NAME]
            nominal: int = int(valute_currency[VALUTE_NOMINAL_FIELD_NAME])
            return round(float(raw_currency_rate.replace(",", ".")) / nominal, 2)


if __name__ == "__main__":
    get_valutes_currencies()
