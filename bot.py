import requests
import misc
import json
from yobit import get_btc
from time import sleep

token = misc.token
# https://api.telegram.org/bot910951170:AAE6G1-rHHxPyp1e6qF2AwgFtAY6Fv-R1DU/sendmessage?chat_id=312925989&text=yebishe

URL = 'https://api.telegram.org/bot' + token + '/'

global last_update_id

last_update_id = 0

def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()

    last_object = data['result'][-1]

    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = data['result'][-1]['message']['chat']['id']
        message_text = data['result'][-1]['message']['text']
        message = {'chat_id': chat_id,
                   'text': message_text}
        return message
    return None


def send_message(chat_id, text='wait a second'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


while True:
    answer = get_message()
    if answer != None:

        chat_id = answer['chat_id']
        text = answer['text']

        if text == '/btc':
            send_message(chat_id, get_btc())
    else:
        continue
    sleep(2)

d = get_updates()
with open('updates.json', 'w') as file:
    json.dump(d, file, indent=2, ensure_ascii=False)
