from central_bank_api.utils import get_valutes_currencies, get_valute_currency_rate


def convert_dollar_to_russian_ruble() -> float:
    VALUTE_CODE = "USD"
    valutes_currencies = get_valutes_currencies()
    return get_valute_currency_rate(VALUTE_CODE, valutes_currencies)


if __name__ == "__main__":
    convert_dollar_to_russian_ruble()