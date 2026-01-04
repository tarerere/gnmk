# 2024/06/18 バージョン
import discord
import os
import datetime
from keep import keep_alive
import asyncio
import time
import logging
from logging import getLogger

logger = getLogger(__name__)
client = discord.Client(intents=discord.Intents.default())

# 定義
# サーバーID(int型)
#じぇねりっくもくり君
JM_ID = "1214572848211955733"
# 崩BWサーバー
HBW_ID = "1262610226826448977"
# 通知させるチャンネルのID
JM_ALERT_CHANNEL = 1214573763526656050
HBW_ALERT_CHANNEL = 1266800353945321548
# 運動部用
SHERE_ID= 1214620402035200060
# テスト用　ALERT_CHANNEL = 1214572849059201045
# 通話参加時のみ付与させるロールのID(@通話中)
JM_ROLE_ID = 1222180449892434120
HBW_ROLE_ID = 1266806710899708057
# 通知をメンションするロールID(@通知OK)
JM_ROLE_ID2 = "1214576516365549578"
HBW_ROLE_ID2 = "1266797184322506752"
# 通知を除外させたいチャンネルID（1：運動用　2：運動後チル）
#JM_LIST_NOALERT_CHANNEL = [1222780507771633715,1248475229593014403]
JM_LIST_NOALERT_CHANNEL1 = [1222780507771633715]
JM_LIST_NOALERT_CHANNEL2 = [1248475229593014403]
HBW_LIST_NOALERT_CHANNEL = [1266825109323386983]
# 通知を除外させたいメンバーID(Rhythmとか)
EXCLUDE_ID = 000000000
# TTS
TTS = True
#now = datetime.utcnow() + timedelta(hours=9)

@client.event
#起動時処理
async def on_ready():
	last_clocked_time = datetime.datetime.now()	
	shere_channel = client.get_channel(SHERE_ID)
	while True:
		#運動部チャンネルに1人でもいたら通知
		# 1時半と2時45分に強制退出
		result = kyouseiKill()
		if result[0] == True:
			await shere_channel.send(result[1], tts=TTS)
			time.sleep(20)
			# チャンネル経由でサーバー内のボイスチャンネル全体を走査
			for ch in shere_channel.guild.voice_channels:
				for member in ch.members:
					if ch.id == result[2].id:
						# move_to(None)で特定のメンバーを切断する
						await member.move_to(None)
							
		last_clocked_time = datetime.datetime.now() #時刻更新処理
		await asyncio.sleep(30)

def kyouseiKill():
	msg = ''
	blnflg = False
	now = datetime.datetime.now()	
	rinfit_channel = client.get_channel(JM_LIST_NOALERT_CHANNEL1)
	cill_channel = client.get_channel(JM_LIST_NOALERT_CHANNEL2)
	kill_channel = None
	
	if len(rinfit_channel.voice_states.keys()) >= 1:
		if int(now.strftime('%Y%m%d%H%M')) >= int(now.strftime('%Y%m%d') + '1730') and int(now.strftime('%Y%m%d%H%M')) <= int(now.strftime('%Y%m%d') + '1635'):
			blnflg = True
			msg = '20秒後に強制退出がまもなく実行されます。本日も運動お疲れ様でした！'
			kill_channel = rinfit_channel
	elif len(cill_channel.voice_states.keys()) >= 1:
		if int(now.strftime('%Y%m%d%H%M')) >= int(now.strftime('%Y%m%d') + '1820') and int(now.strftime('%Y%m%d%H%M')) <= int(now.strftime('%Y%m%d') + '1721'):
			blnflg = True
			msg = '20秒後に強制退出がまもなく実行されます。早く寝てましょう。'
			kill_channel = cill_channel
			
	return blnflg,msg,kill_channel

@client.event
async def on_voice_state_update(member, before, after):
	if after.channel is None:
		return
	# サーバーID(int型)
	if str(member.guild.id) == HBW_ID:
		SERVER_ID = HBW_ID
		LIST_NOALERT_CHANNEL = HBW_LIST_NOALERT_CHANNEL
		ALERT_CHANNEL =  HBW_ALERT_CHANNEL
		ROLE_ID = HBW_ROLE_ID
		ROLE_ID2 = HBW_ROLE_ID2
	else:
		SERVER_ID = JM_ID
		LIST_NOALERT_CHANNEL = JM_LIST_NOALERT_CHANNEL2
		ALERT_CHANNEL = JM_ALERT_CHANNEL
		ROLE_ID = JM_ROLE_ID
		ROLE_ID2 = JM_ROLE_ID2
		
	noalertflg = 0
	for i in LIST_NOALERT_CHANNEL:
		chk_channel = client.get_channel(i)
		if after.channel is not None:
			if after.channel.id == chk_channel.id:
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
