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
		await member.ban()
		await ctx.reply(f"{member.name} was banned.")
		await ctx.message.delete()
	
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def purge(self, ctx, amount:int):
		amount = amount+1
		await ctx.channel.purge(limit=amount)