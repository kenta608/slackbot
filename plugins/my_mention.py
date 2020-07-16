from slackbot.bot import respond_to
from slackbot.bot import listen_to

"""
message.reply():メンション付きで返信
message.send():メッセージを送る
message.react():リアクション(スタンプ)
"""

#respond_toデコレータでメンションを付けて返信ができる
@respond_to('平岡')
def cheer(message):
    message.reply('サウナ')

#listen_toデコレータである発言に対して発言、リアクションさせてみる
@listen_to('いいですか')
def reaction(message):
    message.react('yayagimon')