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

class StaffCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['b','yeet'])
	@commands.has_permissions(administrator=True)
	async def ban(self, ctx, member:discord.Member):
		try:
			await member.ban()
			await ctx.reply(f"**`{member.name}` was banned by `{ctx.author.name}`**")
			await ctx.message.delete()
		except:
			await ctx.reply(f"**Couldn't carry out banish.**")


	@commands.command(aliases=['mute','j','m'])
	@commands.has_permissions(administrator=True)
	async def jail(self, ctx, member:discord.Member):
		jailed = ctx.guild.get_role(1072899313312735293)
		if not jailed in member.roles:
			await member.add_roles(jailed)
			jembed = discord.Embed(description=f"**{member.mention} has been jailed by `{ctx.author.name}`**", color=0x00b0ff, timestamp=ctx.message.created_at)
			await ctx.send(embed=jembed)
			await ctx.message.delete()
		else:
			jembede = discord.Embed(description=f"**{member.mention} is already jailed.**", color=0x00b0ff)
			await ctx.reply(embed=jembede)


	@commands.command(aliases=['uj','unmute','um','release','rel'])
	@commands.has_permissions(administrator=True)
	async def unjail(self, ctx, member:discord.Member):
		jailed = ctx.guild.get_role(1072899313312735293)
		if jailed in member.roles:
			await member.remove_roles(jailed)
			ujembed = discord.Embed(description=f"**`{ctx.author.name}` unjailed {member.mention}!**", color=0x00b0ff, timestamp=ctx.message.created_at)
			await ctx.send(embed=ujembed)
			await ctx.message.delete()
		else:
			ujembede = discord.Embed(description=f"**{member.mention} isn't jailed.**", color=0x00b0ff)
			await ctx.reply(embed=ujembede)


	@commands.command(aliases=['prg'])
	@commands.has_permissions(administrator=True)
	async def purge(self, ctx, amount:int, preason='No given reason.'):
		amount+=1
		def is_me(m):
			return not m.author.id == 504072666718797836
		await ctx.channel.purge(limit=amount, check=is_me,reason=preason)
