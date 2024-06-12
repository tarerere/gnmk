# 2024/06/07 バージョン
import discord
import os
import datetime
from keep import keep_alive
import asyncio
import time

client = discord.Client(intents=discord.Intents.default())

# 定義
# サーバーID(int型)
SERVER_ID = "1214572848211955733"
# 通知させるチャンネルのID
ALERT_CHANNEL = 1214573763526656050
SHERE_ID= 1214620402035200060
#テスト用　ALERT_CHANNEL = 1214572849059201045
# 通話参加時のみ付与させるロールのID
ROLE_ID = '1222180449892434120'
# 通知をメンションするロールID(Rhythmとか)
ROLE_ID2 = "1214576516365549578"
# 通知を除外させたいメンバーID(Rhythmとか)
EXCLUDE_ID = 000000000
# 通知を除外させたいチャンネルID（0：運動用　1：運動後チル）
LIST_NOALERT_CHANNEL = [1222780507771633715,1248475229593014403]
# TTS
TTS = True
#now = datetime.utcnow() + timedelta(hours=9)

@client.event
#起動時処理
async def on_ready():
	last_clocked_time = datetime.datetime.now()	
	shere_channel = client.get_channel(SHERE_ID)
	rinfit_channel = client.get_channel(LIST_NOALERT_CHANNEL[0])
	while True:
		#運動部チャンネルに1人でもいたら通知
		if len(rinfit_channel.voice_states.keys()) >= 1:
			#ここから30秒間隔の処理
			if last_clocked_time.strftime('%H:%M') is not datetime.datetime.now().strftime('%H:%M'):
				# 1時半に強制退出
				if int(datetime.datetime.now().strftime('%H%M')) >= 130 and int(datetime.datetime.now().strftime('%H%M')) <= 135:
					await shere_channel.send('30秒後に強制退出がまもなく実行されます。本日も運動お疲れ様でした！', tts=TTS)
					time.sleep(30)
					talk_channel_id = LIST_NOALERT_CHANNEL[0] 
					# チャンネル経由でサーバー内のボイスチャンネル全体を走査
					for ch in shere_channel.guild.voice_channels:
						for member in ch.members:
							if ch.id == rinfit_channel.id:
								# move_to(None)で特定のメンバーを切断する
								await member.move_to(None)
							
		last_clocked_time = datetime.datetime.now() #時刻更新処理
		await asyncio.sleep(30)

@client.event
async def on_voice_state_update(member, before, after):
	for i in LIST_NOALERT_CHANNEL:
		if after.channel.id == client.get_channel(i).id:
			noalertflg = 1
	# 通話チャンネルの状態を監視、入退室がトリガー
	# 非通知用のチャンネルの場合は処理を終了する。
	if str(member.guild.id) == SERVER_ID and (str(before.channel) != str(after.channel)) and noalertflg == 0:
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
keep_alive()
try:
	client.run(os.environ['TOKEN'])
except:
	os.system("kill")
