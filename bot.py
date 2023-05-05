import telegram
import requests
from pprint import pprint
import logging


url = 'https://dvmn.org/api/long_polling/'
headers = {'Authorization': 'Token 86367ca65496339f9cf298d0532010662722e987'}
timestamp = ''
bot = telegram.Bot(token='5538356450:AAFqsdjOTlkP5pug7BAfYDNGfvbN6XAl4ww')
while True:
    try:
        if timestamp:
            params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, params=params)
            timestamp = ''
        else:
            response = requests.get(url, headers=headers)
        if response.json()['status'] == 'timeout':
            timestamp = response.json()['timestamp_to_request']
        else:
            if response.json()['new_attempts'][0]['is_negative']:
                result = 'К сожалению, в работе нашлись ошибки:('
            else:
                result = 'Преподавателю всё понравилось!'
            text = f'У вас проверили работу "{response.json()["new_attempts"][0]["lesson_title"]}"!\n{result}\n Ссылка: {response.json()["new_attempts"][0]["lesson_url"]}'
            bot.send_message(text=text, chat_id=1509726530)            
    except requests.exceptions.ReadTimeout:
        logging.warning('Превышено время ожидания! Делаю повторный запрос')
    except requests.exceptions.ConnectionError:
        logging.error('Нет подключения к сети!')
