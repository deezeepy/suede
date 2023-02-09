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

class Res(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_message(self, message):
		bad = ['nigg', 'fag']
		for bads in bad:
			if bads in message.content.lower():
				await message.delete()
				try:
					await message.author.send("**You've been jailed for saying awful word!**")
				except:
					pass
				await message.author.ban()
				break
		if message.author.bot is False and not message.content.startswith("!"):
			textmsg = TextBlob(message.content)
			nice = (round(3+(textmsg.sentiment.polarity*2),1))
			state = "N/A"
			if nice < 2:
				state = "Nuisance"
			elif 2 <= nice < 3:
				state = "Questionable"
			elif 3 <= nice < 4:
				state = "Nuetral"
			elif 4 <= nice < 5:
				state = "Pleasant"
			elif nice == 5:
				state = "Saint"
			print(nice)
			print(state + "\n")
		try:
			b = ""
			for a in message.attachments:
				b += f"{a.url} "
			await message.reply(b)
		except:
			pass

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

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		print(before)
		print(after)