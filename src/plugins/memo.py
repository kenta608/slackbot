import pandas as pd
from slackbot.bot import respond_to


def read_memo():
    sauna_csv = pd.read_csv("data/sauna_memo.csv", header=None, index_col=0)
    return sauna_csv


def write_table(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1
    sauna_frame = pd.DataFrame(dic.values(), index=dic.keys())
    sauna_frame.to_csv("data/sauna_memo.csv", header=False)


@respond_to("(.*) 行った")
def memo(message, params):
    # paramsを分解
    sauna_csv = read_memo()
    sauna_dict = sauna_csv.to_dict()[1]
    write_table(sauna_dict, params)

    message.send("記録しました")


@respond_to("行ったところ")
def display(message):
    message.send("これまでに行ったことがある場所です")

    sauna_csv = pd.read_csv("data/sauna_memo.csv", header=None, index_col=0)
    sauna_dict = sauna_csv.to_dict()
    sauna_name_list = list(sauna_dict[1].keys())
    sauna_num = list(sauna_dict[1].values())
    sauna = []
    for i in range(len(sauna_name_list)):
        sauna.append(sauna_name_list[i] + ": " + str(sauna_num[i]))
    # send_user = message.channel._client.users[message.body["user"]]["name"]
    post = {
        "thumb_url": "https://assets.st-note.com/production/uploads/images/24696877/rectangle_large_type_2_18455272374e6f5762b817252b78729c.png?fit=bounds&format=jpeg&quality=45&width=960",  # noqa: E501
        # 'author_name': send_user,
        "text": "\n".join(sauna),
    }
    ret = message._client.webapi.chat.post_message(  # noqa: F841
        message._body["channel"],
        "",
        username=message._client.login_data["self"]["name"],
        as_user=True,
        attachments=[post],
    )
    # ts = ret.body["ts"]
