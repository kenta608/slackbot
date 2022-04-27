import csv

from slackbot.bot import respond_to

EMOJIS = ("one", "two", "three", "four", "five")


@respond_to("poll (.*)")
def poll(message, params):
    # paramsを分解
    args = [row for row in csv.reader([params], delimiter=" ")][0]
    if len(args) < 3:
        message.reply("使用方法: poll 質問 [質問...]")
        return

    # args分解
    options = []
    for i, o in enumerate(args):
        options.append(":{}: {}".format(EMOJIS[i], o))

    # メッセージ作成
    # ref https://github.com/lins05/slackbot/issues/43
    send_user = message.channel._client.users[message.body["user"]]["name"]
    post = {
        "pretext": "<!here> " + "アンケートがあります。".format(send_user),  # noqa: F523
        # 'title': ":sauna_ikitai:",
        "thumb_url": "https://assets.st-note.com/production/uploads/images/24696877/rectangle_large_type_2_18455272374e6f5762b817252b78729c.png?fit=bounds&format=jpeg&quality=45&width=960",  # noqa: E501
        # 'author_name': send_user,
        "text": "\n".join(options),
        "color": "#4999ff",
    }

    # 返信を送る部分
    ret = message._client.webapi.chat.post_message(
        message._body["channel"],
        "",
        username=message._client.login_data["self"]["name"],
        as_user=True,
        attachments=[post],
    )
    ts = ret.body["ts"]

    # ここスタンプ押すところ
    for i, _ in enumerate(options):
        message._client.webapi.reactions.add(
            name=EMOJIS[i], channel=message._body["channel"], timestamp=ts
        )
