import os
from dotenv import load_dotenv
import logging
import random

import telegram
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow_detect_intents import detect_intents_text
from logs_handler import TelegramLogsHandler


logger = logging.getLogger('Logger')


def echo(event, vk_api):
    project_id = os.getenv('DF_PROJECT_ID')
    response = detect_intents_text(project_id, session_id=event.user_id, texts=[event.text])
    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1,1000)
        )


def main():
    load_dotenv()
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_bot = telegram.Bot(telegram_bot_token)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(telegram_bot))

    vk_bot_token = os.getenv('VK_API_TOKEN')
    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()