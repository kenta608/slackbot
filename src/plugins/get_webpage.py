import random

import bs4
import requests


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
    if get_url_web_info.status_code == 200:
        # 検索にヒットしたページ数を取得
        page_num = select_info(get_url_web_info.text, "li.c-pagenation_link a")
        sauna_dict = {}
        for elem in page_num:
            # 各ページでの処理
            page_url = elem.get("href")
            get_url_info = is_exist_webpage(page_url)

            if get_url_info.status_code == 200:
                # サウナの名前とurlをとってくる
                # name_list = []
                names = select_info(get_url_info.text, ".p-saunaItemName h3")
                # page_list = []
                pages = select_info(
                    get_url_info.text, ".p-saunaItem.p-saunaItem--list a"
                )

                check_list_num(names, pages)

                for i in range(len(names)):
                    sauna_dict[names[i].getText().strip()] = pages[i].get(
                        "href"
                    )
    return sauna_dict


if __name__ == "__main__":
    sauna_dict = get_sauna_name_url("中野区")
    # print(sauna_dict)
    print(random.sample(list(sauna_dict.items()), 4))
