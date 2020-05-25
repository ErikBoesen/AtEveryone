import os
import requests
import mebots

from flask import Flask, request

app = Flask(__name__)
bot = mebots.Bot('at_everyone', os.environ.get('BOT_TOKEN'))

SEARCH = '@everyone'


def process(message):
    # Prevent self-reply
    if message['sender_type'] != 'bot':
        if SEARCH in message['text'].lower():



# Endpoint
@app.route('/', methods=['POST'])
def receive():
    message = request.get_json()
    group_id = message["group_id"]
    response = process(message)
    if response:
        send(response, group_id)

    return 'ok', 200


def send(data, group_id):
    url = 'https://api.groupme.com/v3/bots/post'

    data.update({
        'bot_id': bot.instance(group_id).id,
    })
    r = requests.post(url, data=message)


if __name__ == '__main__':
    while True:
        print(process({'text': input('> '), 'sender_type': 'user', 'group_id': None}))
