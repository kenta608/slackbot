import random
from typing import List

import bs4
import requests
from slackbot.bot import respond_to


def is_exist_webpage(url_string):
    """
    webpageが存在するなら、requests.Response()型のオブジェクトを返し、
    そうでないなら、Noneとする
    """
    try:
        get_url_info = requests.get(url_string)
    except requests.exceptions.ProxyError:
        print("存在しないpage")
        get_url_info = requests.Response()
    return get_url_info


def select_info(requests_text, selector):
    """
    指定のwebpageのhtmlからselectorの条件を満たすものを抽出する
    """
    soup = bs4.BeautifulSoup(requests_text, "html.parser")
    elem = soup.select(selector)
    return elem


def check_list_num(names, urls):
    """
    サウナの名前とurlは対応しているはずなので数が同じかどうか確認
    """
    if len(names) != len(urls):
        print("error!!!")
        print("len(names): ", len(names))
        print("len(pages): ", len(urls))


def get_sauna_name_url(keyword):
    """
    keyword:検索ワード
    検索ページのurlからサウナ名とurlを辞書で返す
    """
    # 検索結果
    web_url = "https://sauna-ikitai.com/search?keyword=" + keyword

    get_url_web_info = is_exist_webpage(web_url)
    sauna_dict = {}
    if get_url_web_info.status_code == 200:
        # 検索にヒットしたページ数を取得
        page_num = select_info(get_url_web_info.text, "li.c-pagenation_link a")
        for elem in page_num:
            # 各ページでの処理
            page_url = elem.get("href")
            get_url_info = is_exist_webpage(page_url)

            if get_url_info.status_code == 200:
                # サウナの名前とurlをとってくる
                names = select_info(get_url_info.text, ".p-saunaItemName h3")
                pages = select_info(get_url_info.text, ".p-saunaList a")

                check_list_num(names, pages)

                for i in range(len(names)):
                    sauna_dict[names[i].getText().strip()] = pages[i].get(
                        "href"
                    )
    return sauna_dict


def delete_ng_element(sauna_dict: dict, ng_list: List[str]) -> dict:
    """
    ngワードに指定されたワードを含む辞書を削除するß
    スポーツジム系のサウナを消したい
    """
    ng_keys = []
    for key in sauna_dict.keys():
        for ng_word in ng_list:
            if ng_word in key:
                ng_keys.append(key)
    new_sauna_dict = {k: v for k, v in sauna_dict.items() if k not in ng_keys}
    return new_sauna_dict


# TODO: 複数のキーワードに対応していない
@respond_to("サウナ (.*)")
def suggest_sauna(message, params):
    # paramsを分解
    # TODO: ここの処理を考える (現状できない)
    # args = [row for row in csv.reader([params], delimiter=' ')][0]
    # if len(args) < 1:
    #     message.reply('使用方法: サウナ ~区')
    #     return

    # args
    keyword = params
    sauna_dict = get_sauna_name_url(keyword)
    # print(sauna_dict)
    # ng_listの言葉をkeyに含んでいるものは削除する
    sauna_dict = delete_ng_element(sauna_dict, ["ジム", "スポーツ", "ホテル"])
    # print(sauna_dict)

    sauna_list = random.sample(list(sauna_dict.items()), 4)

    options = []
    for name, url in sauna_list:
        options.append("{}: {}".format(name, url))

    # メッセージ作成
    # ref https://github.com/lins05/slackbot/issues/43
    # send_user = message.channel._client.users[message.body["user"]]["name"]
    post = {
        "pretext": "こちらなんてどうでしょうか",
        "title": "今日のサウナ",
        # 'author_name': send_user,
        "text": "\n".join(options),
        "color": "good",
    }

    # 返信を送る部分

    ret = message._client.webapi.chat.post_message(  # noqa: F841
        message._body["channel"],
        "",
        username=message._client.login_data["self"]["name"],
        as_user=True,
        attachments=[post],
    )
    # ts = ret.body["ts"]

    # # ここスタンプ押すところ
    # for i, _ in enumerate(options):
    #     message._client.webapi.reactions.add(
    #         name=EMOJIS[i],
    #         channel=message._body['channel'],
    #         timestamp=ts
    #     )
