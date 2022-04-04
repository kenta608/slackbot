# coding:utf-8

import schedule
import random

from time import sleep
from plugins.suggest_sauna import get_sauna_name_url
from plugins.slacker import get_slacker


slack = get_slacker()


def get_sauna(params: str) -> dict:
    """
    サウナイキタイのサイトから指定の地域のサウナをランダムで4つ返す
    """
    keyword = params
    sauna_dict = get_sauna_name_url(keyword)
    print(len(sauna_dict))
    sauna_list = random.sample(list(sauna_dict.items()), 4)
    
    options = []
    for name, url in sauna_list:
        options.append('{}: {}'.format(name, url))

    post = {
        # 'pretext': 'サウナ Day',
        'title': params + "のサウナ",
        # 'author_name': send_user,
        'text': '\n'.join(options),
        'color': 'good'
    }
    return post


def recommend_sauna(channel: str):
    """
    指定のチャンネルにメッセージを送る
    """
    nakano_dic = get_sauna("中野区")
    shinjuku_dic = get_sauna("新宿区")
    shibuya_dic = get_sauna("渋谷区")
    slack.chat.post_message(channel, 'さぁ、サウナに行こう', as_user=True)
    slack.chat.post_message(channel, '', as_user=True, attachments=[nakano_dic])
    slack.chat.post_message(channel, '', as_user=True, attachments=[shinjuku_dic])
    slack.chat.post_message(channel, '', as_user=True, attachments=[shibuya_dic])


if __name__ == "__main__":
    schedule.every().friday.at("13:01").do(recommend_sauna, channel='sauna_ikitai')
    print('schedule slack message')
    while True:
        schedule.run_pending()
        sleep(1)
