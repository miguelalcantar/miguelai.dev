import requests
import telegram_ids

def telegram_bot_sendtext(bot_message):
    """Sent a message through a telegram bot
    """

    # credentials
    bot_token = telegram_ids.token
    bot_chatID = telegram_ids.chatID
    # url
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'
    # request
    response = requests.get(send_text)

    return response.json()