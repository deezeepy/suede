import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from discord.utils import get
import asyncio
from discord.ui import Button, View
from discord import app_commands
import requests
import json
import random
from textblob import TextBlob
import datetime

class Res(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		bad = ['nigge', 'fag']
		for bads in bad:
			if bads in message.content.lower():
				await message.delete()
				try:
					await message.author.send("**You've been jailed for saying awful word!**")
				except:
					pass
				await message.author.ban()
				break
		if 'nigga' in message.content and message.author.id == 717762779590688838:
			await message.reply(':face_with_raised_eyebrow:')
		# if message.author.bot is False and not message.content.startswith("!"):
		# 	textmsg = TextBlob(message.content)
		# 	nice = (round(3+(textmsg.sentiment.polarity*2),1))
		# 	state = "N/A"
		# 	if nice < 2:
		# 		state = "Nuisance"
		# 	elif 2 <= nice < 3:
		# 		state = "Questionable"
		# 	elif 3 <= nice < 4:
		# 		state = "Nuetral"
		# 	elif 4 <= nice < 5:
		# 		state = "Pleasant"
		# 	elif nice == 5:
		# 		state = "Saint"
		# 	print(nice)
		# 	print(state + "\n")
	@commands.Cog.listener()
	async def on_message_delete(self, message):
		msgdellogs = self.bot.get_channel(751861618161221792)
		msgdelnoMDs = ['*', '~', '`', '-', '_']
		for dellet in message.content:
			if dellet in msgdelnoMDs:
				message.content = message.content.replace(dellet, "")
		msgdelemb = discord.Embed(description=f"**{message.author.mention} had their message deleted  -** {datetime.datetime.now().strftime('**%I**:**%M**:**%S** **%p**')}\n~~```ansi\n[2;31m{message.content}[0m\n```~~", color = 0xff0000)
		await msgdellogs.send(embed=msgdelemb)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if not before.author.bot and not before.content == after.content:
			msgeditlogs = self.bot.get_channel(751861618161221792)
			msgeditnoMDs = ['*', '~', '`', '-', '_']
			msgeditbna = [before, after]
			for bna in msgeditbna:
				for msgeditlet in bna.content:
					if msgeditlet in msgeditnoMDs:
						bna.content = bna.content.replace(msgeditlet, "")
			msgeditemb = discord.Embed(title=f"**:pencil:  __{before.author.name}__ edited a message in {before.channel.mention}  -**  {datetime.datetime.now().strftime('**%I**:**%M**:**%S** **%p**')}", description=f'**```ansi\n[2;32m[2;36m[2;31m → {before.content}\n[2;36m → {after.content}[0m[2;31m[0m[2;36m[0m[2;32m[0m\n```**:paperclip: [see message](https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id})', color = 0xfcf403)
			await msgeditlogs.send(embed=msgeditemb)
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id == 1071585244345544744:
			dz = self.bot.get_guild(payload.guild_id)
			member = dz.get_role(922825084337532939)
			if not member in payload.member.roles:
				await payload.member.add_roles(member)

			ver = self.bot.get_channel(payload.channel_id)
			verication = await ver.fetch_message(payload.message_id)
			await verication.remove_reaction("<:starGold:917963838496845845>", payload.member)

		if str(payload.emoji) == '<:starGold:917963838496845845>':
			# try:
			channel = self.bot.get_channel(payload.channel_id)
			msg = await channel.fetch_message(payload.message_id)
			print(msg.attachments)
			b = []
			for a in msg.attachments:
				b.append(a.url)
			if len(b) > 0:
				await channel.send("**This picture was added to the starboard!**")
				for url in b:
					await channel.send(url)
			# except:
			# 	pass
	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		# print('BEFORE\n', before, '\n')
		# print('AFTER\n', after, '\n')
		
		vclogs = self.bot.get_channel(751861618161221792)
		vcdesc = ''
		vcemoji = ''
		vcembcol = None
		vcchannelsource = member.voice

		if before.channel is None and not after.channel is None:
			vcdesc = 'joined'
			vcemoji = ':inbox_tray:'
			vcembcol = 0x00ff00
		if not before.channel is None and after.channel is None:	
			vcdesc = 'left'
			vcemoji = ':outbox_tray:' 
			vcembcol = 0xff0000
			vcchannelsource = before

		if after.self_mute is True and before.self_mute is False:
			vcdesc = 'muted in'
			vcemoji = ':mute:'
			vcembcol = 0xff0000
		if after.self_mute is False and before.self_mute is True:
			vcdesc = 'unmuted in'
			vcemoji = ':loud_sound:'
			vcembcol = 0x00ff00
		if after.self_deaf is True and before.self_deaf is False:
			vcdesc = 'deafened in'
			vcemoji = ':headphones:'
			vcembcol = 0xff0000
		if after.self_deaf is False and before.self_deaf is True:
			vcdesc = 'undeafened in'
			vcemoji = ':headphones:'
			vcembcol = 0x00ff00
		if before.self_stream is False and after.self_stream is True:
			vcdesc = 'started streaming in'
			vcemoji = ':movie_camera:'
			vcembcol = 0xffaa00
		if before.self_stream is True and after.self_stream is False:
			vcdesc = 'ended streaming in'
			vcemoji = ':movie_camera:'
			vcembcol = None
		
		if not vcdesc == "":
			vcemb = discord.Embed(description=f"**{vcemoji}   __{member.mention}__ {vcdesc} {vcchannelsource.channel.mention}  -**  {datetime.datetime.now().strftime('**%I**:**%M**:**%S** **%p**')}", color=vcembcol)
			await vclogs.send(embed=vcemb)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		dzserver = self.bot.get_guild(539928737916125184)
		memberrole = dzserver.get_role(922825084337532939)
		await member.add_roles(memberrole)
		jgen = self.bot.get_channel(1070872824685789266)
		await jgen.send(f"**Please welcome {member.mention} to the server!** [{len(member.guild.members)}]")


