import telegram
import requests
from pprint import pprint
import logging
import os
from dotenv import load_dotenv


def main():
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {os.environ["DVMN_TOKEN"]}'}
    timestamp = ''
    params = dict()
    tg_token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_token)
    while True:
        try:
            if timestamp:
                params = {'timestamp': timestamp}
                timestamp = ''
            response = requests.get(url, headers=headers, params=params)
            server_answe = response.json()
            if server_answe['status'] == 'timeout':
                timestamp = server_answe['timestamp_to_request']
            else:
                if server_answe['new_attempts'][0]['is_negative']:
                    result = 'К сожалению, в работе нашлись ошибки:('
                else:
                    result = 'Преподавателю всё понравилось!'
                text = f'У вас проверили работу "{server_answe["new_attempts"][0]["lesson_title"]}"!\n{result}\nСсылка: {server_answe["new_attempts"][0]["lesson_url"]}'
                bot.send_message(text=text, chat_id=chat_id)            
        except requests.exceptions.ReadTimeout:
            logging.warning('Превышено время ожидания! Делаю повторный запрос')
        except requests.exceptions.ConnectionError:
            logging.error('Нет подключения к сети!')


if __name__ == '__main__':
    load_dotenv()
    main()
