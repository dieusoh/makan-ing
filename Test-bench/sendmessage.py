import json
import os
import requests

def lambda_handler(event, context):
    # TODO implement
    BOT_TOKEN = "6566523234:AAGGe36r6_Bqis9BdxHHnRua0kSaBEc_OhQ"
    BOT_CHAT_ID = os.environ.get('CHATID')
    #BOT_CHAT_ID = chat_id
    bot_message = "Hello, this is the bot from telegram"
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHAT_ID + \
                '&parse_mode=HTML&text=' + bot_message
    response = requests.get(send_text)
    print(response)    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }