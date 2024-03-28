# 身内用通話通知bot

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
# TTS
TTS = True


@client.event
async def on_voice_state_update(member, before, after):
  # 通話チャンネルの状態を監視、入退室がトリガー
  if str(member.guild.id) == SERVER_ID and (str(before.channel) != str(
      after.channel)):
      if str(member.guild.id) == SERVER_ID and (str(before.channel) != str(
      after.channel)):
        #now = datetime.utcnow() + timedelta(hours=9)
        # メッセージを送るチャンネル
        alert_channel = client.get_channel(ALERT_CHANNEL)
        if member.id != EXCLUDE_ID:
          # 通話参加時に付与するロールを取得
          role = member.guild.get_role(ROLE_ID)
          # 入室か退室かを判定
          if before.channel is None:
            if member.nick is None:
              msg = '<@&' + ROLE_ID2 + '>' + f'{member.name} が参加しました。'
              await alert_channel.send(msg)
              await member.add_roles(role)
            else:
              msg = '<@&' + ROLE_ID2 + '>' + f'{member.nick} が参加しました。'
              await alert_channel.send(msg, tts=TTS)
              await member.add_roles(role)
          elif after.channel is None:
            if member.nick is None:
              msg = f'{member.name} が退出しました。'
              # await alert_channel.send(msg, tts=TTS)
              await member.remove_roles(role)
            else:
              msg = f'{member.nick} が退出しました。'
              # await alert_channel.send(msg, tts=TTS)
              await member.remove_roles(role)


keep_alive()
try:
  client.run(os.environ['TOKEN'])
except:
  os.system("kill")
