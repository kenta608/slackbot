import requests
import bs4
import random

from slackbot.bot import respond_to


def is_exist_webpage(url_string):
    """
    webpageが存在するなら、requests.Response()型のオブジェクトを返し、
    そうでないなら、Noneとする
    """
    try:
        # get_url_info = requests.get('https://sauna-ikitai.com/search?keyword=中野')
        # get_url_info = requests.get('https://sauna-ikitai.com/saunas/1754')
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
    web_url = 'https://sauna-ikitai.com/search?keyword=' + keyword

    get_url_web_info = is_exist_webpage(web_url)
    sauna_dict = {}
    if get_url_web_info.status_code == 200:
        # 検索にヒットしたページ数を取得
        page_num = select_info(get_url_web_info.text, 'li.c-pagenation_link a')
        for elem in page_num:
            # 各ページでの処理
            page_url = elem.get('href')
            get_url_info = is_exist_webpage(page_url)

            if get_url_info.status_code == 200:
                # サウナの名前とurlをとってくる
                name_list = []
                names = select_info(get_url_info.text, '.p-saunaItemName h3')
                page_list = []
                pages = select_info(get_url_info.text, '.p-saunaItem.p-saunaItem--list a')

                check_list_num(names, pages)                

                for i in range(len(names)):
                    sauna_dict[names[i].getText().strip()] = pages[i].get('href')
    return sauna_dict


#TODO: 複数のキーワードに対応していない
@respond_to('サウナ (.*)')
def suggest_sauna(message, params):
    # paramsを分解
    #TODO: ここの処理を考える (現状できない)
    # args = [row for row in csv.reader([params], delimiter=' ')][0]
    # if len(args) < 1:
    #     message.reply('使用方法: サウナ ~区')
    #     return

    # args
    keyword = params
    sauna_dict = get_sauna_name_url(keyword)
    sauna_list = random.sample(list(sauna_dict.items()), 4)
    
    options = []
    for name, url in sauna_list:
        options.append('{}: {}'.format(name, url))
   
    # メッセージ作成
    # ref https://github.com/lins05/slackbot/issues/43
    send_user = message.channel._client.users[message.body['user']][u'name']
    post = {
        'pretext': 'こちらなんてどうでしょうか',
        'title': "今日のサウナ",
        # 'author_name': send_user,
        'text': '\n'.join(options),
        'color': 'good'
    }

    # 返信を送る部分
    ret = message._client.webapi.chat.post_message(
        message._body['channel'],
        '',
        username=message._client.login_data['self']['name'],
        as_user=True,
        attachments=[post]
    )
    ts = ret.body['ts']

    
    
    
    # # ここスタンプ押すところ
    # for i, _ in enumerate(options):
    #     message._client.webapi.reactions.add(
    #         name=EMOJIS[i],
    #         channel=message._body['channel'],
    #         timestamp=ts
    #     )
