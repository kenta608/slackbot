from slackbot.bot import respond_to
import csv

EMOJIS = (
    'one',
    'two',
    'three',
    'four',
    'five'
)

@respond_to('poll (.*)')
def poll(message, params):
    # paramsを分解
    args = [row for row in csv.reader([params], delimiter=' ')][0]
    if len(args) < 3:
        message.reply('使用方法: poll 質問 [質問...]')
        return

    # args分解
    options = []
    for i, o in enumerate(args):
        options.append(':{}: {}'.format(EMOJIS[i], o))

    # メッセージ作成
    # ref https://github.com/lins05/slackbot/issues/43
    send_user = message.channel._client.users[message.body['user']][u'name']
    post = {
        'pretext': '@here' + '{}さんからアンケートがあります。'.format(send_user),
        'title': "今日のサウナ",
        'author_name': send_user,
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

    # ここスタンプ押すところ
    for i, _ in enumerate(options):
        message._client.webapi.reactions.add(
            name=EMOJIS[i],
            channel=message._body['channel'],
            timestamp=ts
        )