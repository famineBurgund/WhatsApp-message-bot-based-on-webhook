import logging
import time

import requests


def get_pact_conversation_id(company_id, auth_token, phone, retries=3, delay=2):
    """
    Получение conversation ID для клиента с поддержкой повторных попыток при сбое.

    :param company_id: ID компании для API Pact
    :param auth_token: Токен для авторизации в API Pact
    :param phone: Номер телефона клиента
    :param retries: Количество повторных попыток при сбое
    :param delay: Начальная задержка между попытками (в секундах), увеличивается экспоненциально
    :return: conversation ID или None в случае ошибки
    """
    api_endpoint = f"https://api.pact.im/p1/companies/{company_id}/conversations"
    headers = {
        "X-Private-Api-Token": auth_token,
        "Content-Type": "application/json"
    }
    data = {
        "provider": "whatsapp",
        "phone": phone
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(api_endpoint, headers=headers, json=data)

            # Обработка успешного ответа
            if response.status_code == 200:
                response_data = response.json()
                if 'data' in response_data and 'conversation' in response_data['data']:
                    conversation_id = response_data['data']['conversation']['external_id']
                    logging.info(f"Беседа создана! Conversation ID: {conversation_id}")
                    return conversation_id
                else:
                    logging.error(f"Ошибка данных в ответе: {response_data}")
                    return False

            # Обработка статуса 202 (запрос в процессе)
            elif response.status_code == 202:
                logging.info("Запрос всё ещё в процессе")
                return False

            # Обработка других кодов состояния
            else:
                logging.error(f"Ошибка: {response.status_code}, {response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка сети или запроса: {e}")

        # Логика повторной попытки
        if attempt < retries:
            logging.warning(f"Повторная попытка {attempt} из {retries}. Ожидание {delay} сек.")
            time.sleep(delay)
            delay *= 2  # Экспоненциальное увеличение времени ожидания
        else:
            logging.error(f"Превышено количество попыток {retries}. Запрос не выполнен.")

    return False


def send_whatsapp_message_via_pact(company_id, phone_number, message, auth_token, retries=3, delay=2,
                                   timeout=10):
    """
    Отправка сообщения через WhatsApp API Pact с поддержкой повторных попыток и тайм-аутов.

    :param company_id: ID компании для API Pact
    :param phone_number: Номер телефона получателя
    :param message: Сообщение для отправки
    :param auth_token: Токен авторизации Pact API
    :param retries: Количество попыток в случае неудачи
    :param delay: Задержка между повторными попытками (в секундах), увеличивается экспоненциально
    :param timeout: Тайм-аут для запроса (в секундах)
    :return: True, если сообщение отправлено успешно, иначе False
    """

    conversation_id = get_pact_conversation_id(company_id, auth_token, phone_number)

    api_endpoint = f"https://api.pact.im/p1/companies/{company_id}/conversations/{conversation_id}/messages"
    headers = {
        "X-Private-Api-Token": auth_token,
        "Content-Type": "application/json"
    }
    data = {
        "message": message,
        "phone_number": phone_number
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(api_endpoint, headers=headers, json=data, timeout=timeout)

            if response.status_code == 200:
                logging.info(f"Сообщение успешно отправлено на {phone_number}!")
                return True
            elif response.status_code in (400, 403, 404):
                # Обработка клиентских ошибок, повторные попытки не помогут
                logging.error(f"Ошибка клиента {response.status_code}: {response.text}")
                return False
            elif response.status_code in (500, 502, 503, 504):
                # Серверные ошибки, можно попробовать снова
                logging.warning(
                    f"Серверная ошибка {response.status_code}, повторная попытка отправки на {phone_number}")
            else:
                logging.error(f"Неизвестная ошибка {response.status_code}: {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка запроса при отправке сообщения на {phone_number}: {e}")

        # Повторная попытка с задержкой
        if attempt < retries:
            logging.warning(f"Повторная попытка {attempt} из {retries}. Ожидание {delay} секунд.")
            time.sleep(delay)
            delay *= 2  # Экспоненциальное увеличение времени ожидания
        else:
            logging.error(f"Превышено количество попыток {retries}. Сообщение на {phone_number} не отправлено.")

    return False