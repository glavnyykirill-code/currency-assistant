import requests
from datetime import datetime
from langchain_classic.tools import tool

API_BASE_URL = "https://api.frankfurter.app"


@tool
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    date: str = "latest",
) -> dict:
    """
    Convert currencies using the public Frankfurter API.

    Use this tool for ANY request where the user wants to convert money
    from one currency to another.

    Arguments:
    - amount: positive number
    - from_currency: 3-letter ISO code of the source currency (e.g. USD, EUR, RUB)
    - to_currency: 3-letter ISO code of the target currency (e.g. USD, EUR, RUB)
    - date: 'latest' or specific date in 'YYYY-MM-DD' format

    Returns:
    A dict with keys:
    - amount: исходная сумма
    - from_currency: исходная валюта
    - to_currency: целевая валюта
    - date: дата курса
    - rate: курс 1 from_currency в to_currency
    - converted_amount: итоговая сумма в целевой валюте
    - error: текст ошибки (если что-то пошло не так)
    """
    try:
        if amount <= 0:
            return {"error": "Amount must be positive."}

        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        if date and date.lower() != "latest":
            from datetime import datetime
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {
                    "error": f"Invalid date format: {date}. Use 'YYYY-MM-DD' or 'latest'."
                }

        if not date or date.lower() == "latest":
            url = f"{API_BASE_URL}/latest"
        else:
            url = f"{API_BASE_URL}/{date}"

        params = {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
        }

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if "rates" not in data or to_currency not in data["rates"]:
            return {
                "error": f"Cannot get rate for {to_currency}. Full response: {data}"
            }

        converted_amount = float(data["rates"][to_currency])
        base_amount = float(data.get("amount", amount))

        if base_amount == 0:
            return {
                "error": "API returned 0 base amount, cannot compute rate.",
            }

        rate = converted_amount / base_amount

        return {
            "amount": base_amount,
            "from_currency": data.get("base", from_currency),
            "to_currency": to_currency,
            "date": data.get("date", date),
            "rate": rate,
            "converted_amount": converted_amount,
        }

    except requests.RequestException as e:
        return {"error": f"API_ERROR: {str(e)}"}
    except Exception as e:
        return {"error": f"UNEXPECTED_ERROR: {str(e)}"}