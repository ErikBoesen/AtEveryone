import os
import requests
import mebots

from flask import Flask, request

app = Flask(__name__)
bot = mebots.Bot('at_everyone', os.environ.get('BOT_TOKEN'))
GROUPME_ACCESS_TOKEN = os.environ.get('GROUPME_ACCESS_TOKEN')
SEARCH = '@everyone'


def get_user_ids(group_id):
    users = requests.get(f'https://api.groupme.com/v3/groups/{group_id}?token={GROUPME_ACCESS_TOKEN}').json()['response']['members']
    user_ids = [user['id'] for user in users]
    return user_ids


def send(message):
    url = 'https://api.groupme.com/v3/bots/post'
    r = requests.post(url, data=message)


def process(message):
    # Prevent self-reply
    if message['sender_type'] != 'bot':
        if SEARCH in message['text'].lower():
            group_id = message['group_id']
            user_ids = get_user_ids(group_id)
            response = {
                'bot_id': bot.instance(group_id).id,
                'text': '@everyone',
                'attachments': [{
                    'loci': [[0, 9]] * len(user_ids),
                    'type': 'mentions',
                    'user_ids': user_ids
                }]
            }
            return response


# Endpoint
@app.route('/', methods=['POST'])
def receive():
    message = request.get_json()
    response = process(message)
    if response:
        send(response)

    return 'ok', 200


if __name__ == '__main__':
    while True:
        print(process({'text': input('> '), 'sender_type': 'user', 'group_id': 49940116}))
