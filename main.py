# 2024/04/23 バージョン
import discord
import os
from datetime import datetime, timedelta
from keep import keep_alive

client = discord.Client(intents=discord.Intents.default())

# 定義
# サーバーID(int型)
SERVER_ID = "1214572848211955733"
# 通知させるチャンネルのID
ALERT_CHANNEL = 1214573763526656050
#テスト用　ALERT_CHANNEL = 1214572849059201045
# 通話参加時のみ付与させるロールのID
ROLE_ID = 1222180449892434120
# 通知をメンションするロールID(Rhythmとか)
ROLE_ID2 = "1214576516365549578"
# 通知を除外させたいメンバーID(Rhythmとか)
EXCLUDE_ID = 000000000
# 通知を除外させたいチャンネルID
NOALERT_CHANNEL = '1222780507771633715'
# TTS
TTS = True
#now = datetime.utcnow() + timedelta(hours=9)

@client.event
async def on_voice_state_update(member, before, after):
  # 通話チャンネルの状態を監視、入退室がトリガー
  # 非通知用のチャンネルの場合は処理を終了する。

  if str(member.guild.id) == SERVER_ID and (str(before.channel) != str(after.channel)) and str(after.channel.id) != NOALERT_CHANNEL:
    # メッセージを送るチャンネル
    alert_channel = client.get_channel(ALERT_CHANNEL)
    if member.id != EXCLUDE_ID:
      # 通話参加時に付与するロールを取得
      role = member.guild.get_role(ROLE_ID)
      # 入室か退室かを判定
      if before.channel is None:
        await member.add_roles(role)
        if len(after.channel.members) == 1:
            if member.nick is None:
              msg = '<@&' + ROLE_ID2 + '>' + f'{after.channel.name} に ' + f'{member.name} が参加しました。'
              await alert_channel.send(msg)
            else:
              msg = '<@&' + ROLE_ID2 + '>' + f'{after.channel.name} に ' + f'{member.nick} が参加しました。'
              await alert_channel.send(msg, tts=TTS)
      elif after.channel is None:
        await member.remove_roles(role)
        #メッセージを削除する
        # def delete_messages(,,,):

keep_alive()
try:
  client.run(os.environ['TOKEN'])
except:
  os.system("kill")
