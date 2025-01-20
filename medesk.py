import logging
import time
import pandas as pd
import requests

from io import StringIO


def get_data_from_medesk(url, retries=3, delay=2, timeout=10):
    """
    Загружает данные с указанного URL с повторными попытками при неудаче.

    :param url: URL для загрузки данных
    :param retries: Количество повторных попыток
    :param delay: Задержка между попытками (в секундах)
    :param timeout: Тайм-аут для каждого запроса
    :return: DataFrame с загруженными данными или None в случае ошибки
    """
    logging.info(f"Загружаем данные из Medesk...")

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            logging.info(f"Получен ответ от сервера на попытке {attempt}: {response.status_code}")

            if response.status_code == 200:
                return pd.read_csv(StringIO(response.text))
            else:
                logging.error(f"Ошибка при загрузке данных из Medesk: {response.status_code}, {response.text}")
                if response.status_code in [500, 502, 503, 504]:
                    logging.warning(f"Серверная ошибка. Попытка {attempt} из {retries}. Ожидание {delay} секунд.")
                    time.sleep(delay)
                else:
                    break  # Не повторяем попытки для клиентских ошибок

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при загрузке данных: {e}")
            if attempt < retries:
                logging.warning(f"Повторная попытка {attempt} из {retries}. Ожидание {delay} секунд.")
                time.sleep(delay)
            else:
                logging.error("Превышено количество попыток загрузки данных. Данные из Medesk не загружены")

    return None
