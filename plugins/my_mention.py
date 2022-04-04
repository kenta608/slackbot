from slackbot.bot import respond_to
from slackbot.bot import listen_to
import numpy as np

"""
message.reply():メンション付きで返信
message.send():メッセージを送る
message.react():リアクション(スタンプ)
"""


#respond_toデコレータでメンションを付けて返信ができる
@respond_to('平岡')
def hiraoka(message):
    message.react('sugu_hiraoka')
    message.react('hiraoka_sauna')


#respond_toデコレータでメンションを付けて返信ができる
@respond_to('神谷')
def kamiya(message):
    random_num = np.random.randint(0, 2)
    # fname: slack上で表示するファイル名
    # fpath: ファイルが置いてあるパス
    # initial_comment: slack上で表示するコメント
    if random_num == 0:
        message.channel.upload_file(fname="kamiya", fpath="data/kamiya.jpg", initial_comment="神谷さんです")
    else:
        message.channel.upload_file(fname="kamiya", fpath="data/kamiya2.png", initial_comment="神谷さんです")


#listen_toデコレータである発言に対して発言、リアクションさせてみる
@listen_to('いいですか')
def reaction(message):
    message.react('yayagimon')
