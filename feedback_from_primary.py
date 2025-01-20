import logging
import random
import pandas as pd
from aiogram import Bot
import asyncio

from utils.medesk import get_data_from_medesk
from utils.pact import get_pact_conversation_id, send_whatsapp_message_via_pact

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# данные для Pact
company_id = "..."
auth_token = "..."

# данные для Telegram бота
token = "..."  #

chat_id = "..." 



# Функция для нормализации номера телефона
def normalize_phone_number(phone_number):
    phone_number = phone_number.strip()

    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number  # Добавляем код страны, если не указан

    if phone_number.startswith('+8'):
        phone_number = phone_number.replace('+8', '+7', 1)

    return phone_number

# Объявим множество для хранения статуса отправки сообщений
valid_phone_numbers = set()

# Основная логика обработки данных
async def main():
    url = "https://app.medesk.net/hooks/.../"
    data = get_data_from_medesk(url)

    if data is not None:
        # Фильтрация DataFrame
        try:
            df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

            filtered_df = df[(~df['Метки'].str.contains('BAD', na=False)) & (df['Категория'] == 'Первичный')]
            logging.info(f"Найдено {len(filtered_df)} записей для обработки.")

            for _, row in filtered_df.iterrows():
                try:
                    phone_number = normalize_phone_number(str(row['Телефон']))
                    name = str(row['Полное имя']).strip()
                    DocDate = str(row['Дата приема']).strip()
                    logging.info(f"----")
                    logging.info(f"Обработанный номер: {phone_number}, Имя: {name}")

                    # Получаем conversation_id для текущего клиента
                    conversation_id = get_pact_conversation_id(company_id, auth_token, phone_number)

                    if conversation_id is not None:
                        message = f"""
                        Здравствуйте, {name}!\n\
                        \n\
                        Вчера, ({DocDate}), вы были на первичном приёме у врача-косметолога в нашей клинике. 
                        Пожалуйста, уделите 2 минуты и поделитесь впечатлением о приёме. Это анонимно.\n\
                        \n\
                        Ссылка: \n\
                        https://...
                        """

                        # send_whatsapp_message_via_pact(company_id, phone_number, message)

                        # Задержка от 5 до 10 секунд
                        delay = random.randint(5, 10)
                        await asyncio.sleep(delay)
                        logging.info(f"Оправляем сообщения через WhatsApp на номер {phone_number}")
                    else:
                        logging.error(f"Не удалось создать беседу для {phone_number}")
                        valid_phone_numbers.add(phone_number)

                except Exception as e:
                    logging.error(f"Ошибка при обработке строки: {row}. Причина: {e}")

        except Exception as e:
            logging.error(f"Ошибка при фильтрации данных: {e}")

    else:
        logging.error("Не удалось загрузить данные для обработки.")
    logging.info(f"----")



    bot = Bot(token=token)

    values = [f'Отправлен запрос обратной связи от первичных пациентов - {len(filtered_df)} шт:\n']
    print (valid_phone_numbers)

    for _, row in filtered_df.iterrows():
        phone_number = str(row['Телефон']).strip()
        name = str(row['Полное имя']).strip()
        fam = name.split()[0]
        message1 = f"{phone_number}, {fam}"

        # Проверяем статус отправки сообщения
        if phone_number in valid_phone_numbers:
            values.append('❌' + message1)
        else:
            values.append('✅' + message1)

    text = "\n".join(values)
    logging.info("Отправка сообщений через Telegram")
    await bot.send_message(chat_id, text)


if __name__ == '__main__':
    asyncio.run(main())
