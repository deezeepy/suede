import discord
import os
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import res, mod
from discord.utils import get
import asyncio
from discord.ui import Button, View
from discord import app_commands
import requests
import json
import random
from textblob import TextBlob
import datetime
import time
from traceback import print_exc
import re
from PIL import Image, ImageFont, ImageDraw, ImageOps
from webcolors import hex_to_rgb
import urllib.request
from math import *
from PyDictionary import PyDictionary
from decimal import *

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
	print(f"\n{bot.user.name}!\n")
	playin = discord.Activity(name='Connect 4', type=discord.ActivityType.playing, details='lol')
	gen = bot.get_channel(1070872824685789266)
	await bot.change_presence(activity=playin, status=discord.Status.idle)
	dzguild = bot.get_guild(539928737916125184)
	dzrole = dzguild.get_role(824670964762804284)
	noxp = dzguild.get_role(1137140154360942624)
	while True:
		with open('spamcheck.json','r+',encoding='utf-8') as scraw:
			sc = json.load(scraw)
			for a in sc:
				msga = dzguild.get_member(int(a))
				spamchan = bot.get_channel(sc[a][1])
				if sc[a][0] > 3:
					if msga.top_role.position < 21:
						def is_msga(m):
							return m.author == msga
						await spamchan.purge(limit=sc[a][0], check=is_msga)
						await spamchan.send(f"**{msga.mention}, please stop spamming the chat <:emojiYawn:552169910130704394> [`{sc[a][0]} messages in 3 seconds.`]**")
				if not sc[a][0] > 3 and not noxp in msga.roles and str(spamchan.type) == 'text':
					with open('lvls.json','r+',encoding='utf-8') as lvlsraw:
						lvls = json.load(lvlsraw)
						if not str(msga.id) in str(lvls):
							lvls[str(msga.id)] = [1,25,0]
							await spamchan.send(f"{msga.mention} <:lvlup:1136150865225449474> **__First Level Up__!  [`{lvls[str(msga.id)][0]}`] `Your XP Boost: {lvls[str(msga.id)][0]/10}%`**")
						else:
							xpperc = (lvls[str(msga.id)][0] / 1000) +1

							newxp = (Decimal(str(lvls[str(msga.id)][1])) + (Decimal(str(xpperc))*25))
							newlvlxp = (Decimal(str(lvls[str(msga.id)][2])) + (Decimal(str(xpperc))*25))

							lvls[str(msga.id)][1] = float(newxp)
							lvls[str(msga.id)][2] = float(newlvlxp)
							with open('lvlxpgoals.txt','r') as lxlxpgoalsraw:
								lxlxpgoals = eval(lxlxpgoalsraw.read())
								if lvls[str(msga.id)][2] >= lxlxpgoals[lvls[str(msga.id)][0]]:
									lvls[str(msga.id)][2] = float(Decimal(str(lvls[str(msga.id)][2])) - lxlxpgoals[lvls[str(msga.id)][0]])
									lvls[str(msga.id)][0]+=1
									await spamchan.send(f"{msga.mention} <:lvlup:1136150865225449474> **__Level Up__!  [`{lvls[str(msga.id)][0]}`] XP Boost: `{lvls[str(msga.id)][0]/10}%`**")
						lvlsraw.seek(0)
						json.dump(lvls, lvlsraw, indent=4)
						lvlsraw.truncate()

					
			sc = {}
			scraw.seek(0)
			json.dump(sc,scraw,indent=4)
			scraw.truncate()
			await asyncio.sleep(3)
# 	while True:
# 		await dzrole.edit(color=0xff3c3c)
# 		await asyncio.sleep(2)
# 		await dzrole.edit(color=0x00b0ff)
# 		await asyncio.sleep(2)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		msg = '**This command is still on cooldown for another __{:.2f} seconds__!**'.format(error.retry_after)
		await ctx.send(msg)
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send("**Error: `That command does not exist.`**")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Error: `You are missing a part of your command.`**")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("**Error: `That is an ADMIN command!`**")
	elif isinstance(error, commands.errors.ChannelNotFound):
		await ctx.send("**Error: `That channel doesn't exist.`**")
	elif isinstance(error, commands.errors.RoleNotFound):
		await ctx.send("**Error: `Couldn't find role.`**")
	elif isinstance(error, commands.errors.TooManyArguments):
		await ctx.send(f"**Error: `Unwanted details in command. ({error.args})`**")
	elif isinstance(error, commands.errors.UserNotFound):
		await ctx.send("**Error: `Couldn't find member.`**")
	elif isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
		await ctx.send("**Make sure that quotations are aren't touching other elements in your command.**")
	else:
		try:
			print(error)
			print(type(error))
			await ctx.send(f"`{error}`")
		except:
			pass
	print(error)
	print(type(error))

@bot.command(aliases=["p","ms"])
async def ping(ctx):
	pin = round(bot.latency*1000)
	if 0 < pin < 150:
		status = "Great!"
	if 150 < pin < 300:
		status = "A bit slow."
	if 300 < pin < 500:
		status = "Yikes."
	if 500 < pin < 900:
		status = "Wayyy too slow."
	if 1000 < pin:
		status = "Something is terribly wrong."
	await ctx.reply(f'**{round(bot.latency * 1000)}ms (`{status}`)**')
	if ctx.message.content == '!ping':
		await ctx.message.delete()


###############################################################################




@bot.command(aliases=['l','lvl','lvls','levels'])
async def level(ctx):
	with open('lvls.json','r+',encoding='utf-8') as levelsraw:
		levels = json.load(levelsraw)
		if str(ctx.author.id) in str(levels):
			with open('lvlxpgoals.txt','r') as levelxpgoalsraw:
				levelxpgoals = eval(levelxpgoalsraw.read())
				levelembed = discord.Embed(title=f"**{ctx.author.name}**",description=f"**Level `{levels[str(ctx.author.id)][0]}`\nXP: `{round(levels[str(ctx.author.id)][2],1)} / {levelxpgoals[levels[str(ctx.author.id)][0]]}`\nTotal XP: `{round(levels[str(ctx.author.id)][1],1)}`\nYOUR BOOST: `{levels[str(ctx.author.id)][0] / 10}%`**", color=ctx.author.color)
				levelembed.set_thumbnail(url=ctx.author.avatar)
				await ctx.reply(embed=levelembed)
		else:
			await ctx.reply("**You aren't leveled yet :( Type in chat receive your first level.!**")


	# await ctx.reply('<:yellowdollarsignyoutube:1130852475893715105>')
	# while True:
	# 	try:
	# 		print('go')
	# 		message = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
	# 		if message.content == 'stop':
	# 			print('yay you stopped the timebomb')
	# 			break
	# 		else:
	# 			print('nah, try again')
	# 	except asyncio.TimeoutError:
	# 		print('boom, ur  now dead')
	# 		break

# @bot.command()
# @commands.is_owner()
# async def timer(ctx):
# 	timerthen = datetime.datetime.now()
# 	await ctx.reply("**Your timer has started!**")
# 	while True:
# 		timerstop = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
# 		if timerstop.content == 'timer stop':
# 			timerres = datetime.datetime.now()-timerthen
# 			print(f"{timerres.min} minutes and {timerres.seconds}.{round(timerres.microseconds/10000)} seconds")
# 			print(timerres.microseconds)
# 			break

@bot.command()
@commands.is_owner()
async def customsay(ctx):
	await ctx.send("@everyone")
	await ctx.send("We're singing Barbie Girl.")
	await ctx.send("But if any of you screws up...")
	await ctx.send("You get instantly banned.")

@bot.command()
@commands.is_owner()
async def ds(ctx):
	lyricschan = bot.get_channel(1134125877647655103)
	lyricsrole = ctx.guild.get_role(1134132685447630859)
	with open('lyrics.txt','r') as lyrics:
		strlyrics = lyrics.read()
		lyricssplit = strlyrics.splitlines()
	await ctx.send("**Welcome to Discord Sings Barbie Girl by Aqua!**")
	while True:
		lyricsfinish = None
		lyrics_role_members = lyricsrole.members
		lyrics_role_members2 = lyricsrole.members
		lyrics_singer_present = []
		while True:
			lyricsretry = await bot.wait_for('message', check=lambda message: message.channel == ctx.channel)
			if lyricsretry.content.lower() == 'here':
				if not lyricsretry.author.top_role == lyricsrole and not lyricsretry.author == ctx.author:
					await lyricsretry.reply("**Sorry big guy, you can't take part in this with __Administrator__ perms.**")
				elif lyricsretry.author in lyrics_singer_present:
					await lyricsretry.reply("**You've already been added to queue.**")
				else:
					lyrics_singer_present.append(lyricsretry.author)
					await lyricsretry.reply("**You've been added to the singer queue! Get ready!**")
			if lyricsretry.content == 'START-SINGING' and lyricsretry.author == ctx.author:
				break

		if len(lyrics_singer_present) > 0:
			lyrics_singer_liststr = ""
			# lyrics_order_num = 1

			for lyrics_role_member in lyrics_role_members:
				if not lyrics_role_member in lyrics_singer_present:
					lyrics_role_members2.remove(lyrics_role_member)
				else:
					lyrics_singer_liststr+=f"**{lyrics_role_members2.index(lyrics_role_member)+1}**. {lyrics_role_member.mention}\n"
					# lyrics_order_num+=1

			await ctx.send(f'**We are all set and ready to start in `15 seconds`! Get your script ready!\n\nThis** is the **singing order** for this round. It will **loop** until the final lyric.\n{lyrics_singer_liststr}\nWhen it is your turn, you have **`60 seconds`** to send the **next line of lyrics** in {lyricschan.mention}')
			await asyncio.sleep(10)
			for lyrics_CD in range(1,6):
				await ctx.send(f"**Starting in {lyrics_CD}...**")
				await asyncio.sleep(1)
			await ctx.send("**Action!**")

			lyric = -1
			while True:
				for lyric_singer in lyrics_role_members2:
					print(lyric_singer)
					lyric+=1
					strlyric = lyricssplit[lyric]
					if strlyric.startswith("*"):
						await ctx.send(strlyric)
						lyric+=1
						strlyric = lyricssplit[lyric]

					try:
						await asyncio.sleep(0.5)
						lyricsmsg = await bot.wait_for('message', check=lambda message: message.channel == ctx.channel, timeout=60)
						await asyncio.sleep(0.5)
						sstrlyric = strlyric
						strlyric = "".join(re.findall("[a-zA-Z]+",strlyric.lower()))
						lyricsmsg.content = "".join(re.findall("[a-zA-Z]+",lyricsmsg.content.lower()))

					except asyncio.TimeoutError:
						lyricsfinish = False
						await ctx.send(f"**{lyricsmsg.author.mention} took too long (`60 seconds`) and was banned.**")
						break
					print(strlyric)
					print(lyricsmsg.content, '\n')
					if not lyricsmsg.author == lyric_singer:
						lyricsfinish = False
						await lyricsmsg.author.remove_roles(lyricsrole)
						await ctx.send(f"**{lyricsmsg.author.mention} was banned.\n\n*It was {lyric_singer.mention}'s turn!***")
						break
					elif not strlyric in lyricsmsg.content:
						lyricsfinish = False
						await lyricsmsg.author.remove_roles(lyricsrole)
						await ctx.send(f"**{lyricsmsg.author.mention} was banned.\n\nHe was supposed to say:**\n *\" {sstrlyric} \"*")
						break
					elif strlyric in lyricsmsg.content and strlyric == 'ohiloveyouken':
						lyricsfinish = True
						break
				if lyricsfinish is False:
					break
		if lyricsfinish is True:
			break
	await ctx.send("**THAT'S A WRAP!! :clap: :clap: :clap:**")




@bot.command(aliases=["c4","connectfour"])
@commands.cooldown(1,60,commands.BucketType.member)
async def connect4(ctx,c4p2m:discord.Member):
	if c4p2m == ctx.author:
		await ctx.reply("**You cannot 1v1 yourself.**")
	elif c4p2m.bot:
		await ctx.reply("**Although it would be awesome, bots like me cannot play Connect 4 with you. Please use an ID or @ of a __human__!**")
	else:
		c4p1m = ctx.message.author
		c4accmsg = await ctx.reply(f"**{c4p2m.mention}, do you accept {c4p1m.display_name}'s __Connect 4__ request? `type y or n`**")
		gc4 = False
		while True:
			try:
				message = await bot.wait_for('message', check=lambda message: message.author == c4p2m, timeout=60)
				if message.content.lower() == 'n' or message.content.lower() == 'no':
					rejc4 = ["well this is awkward.","Rejected!","Ouch!","I guess he's busy.","Oh well."]
					await message.reply(f"**{random.choice(rejc4)}** {c4p1m.mention}")
					break
				if message.content.lower() == 'y' or message.content.lower() == 'yes':
					accc4 = ["Let's go....","Working on it....","Getting started..","We're setting up the game..."]
					welcome = await ctx.send(f"**{random.choice(accc4)}** {c4p1m.mention}")
					gc4 = True
					break
			except asyncio.TimeoutError:
				norespc4 = ["We'll take that as a no.","........","Timer has run out, game cancelled."]
				await c4accmsg.reply(f"**{random.choice(norespc4)}**")
				break
		if gc4 is True:
			strints = ['1','2','3','4','5','6','7']
			a = []
			b = []
			c = []
			d = []
			e = []
			f = []
			c4p1 = []
			c4p2 = []
			c4ps = [c4p1,c4p2]
			strabcs = [a,b,c,d,e,f]
			rstrabcs=['a','b','c','d','e','f']
			rrstrabcs = rstrabcs[::-1]
			c4intsem = ["<:c41:1130937256232878272>", "<:c42:1130937265632313404>", "<:c43:1130937258829152316>", "<:c44:1130937267779801249>", "<:c45:1130937260653682768>", "<:c46:1130937269516251169>", "<:c47:1130937263560335571>"]
			c4intsr = ["<:c4r1:1131218620454817973>", "<:c4r2:1131218549080334477>", "<:c4r3:1131218547209666630>", "<:c4r4:1131218542218465330>", "<:c4r5:1131218540515561482>", "<:c4r6:1131218534756790303>", "<:c4r7:1131218533221670992>"]
			c4intsy = ["<:c4y1:1131218619183927446>", "<:c4y2:1131218647243825182>", "<:c4y3:1131218545179643914>", "<:c4y4:1131218543732596787>", "<:c4y5:1131218538972061817>", "<:c4y6:1131218536719716463>", "<:c4y7:1131218531271331840>"]

			if random.randint(1,2) == 2:
				c4ps.reverse()
			c4well = 0
			while True:
				for c4p in c4ps:
					board = ''
					if c4p is c4p1:
						c4pmen = c4p1m
						c4poth = c4p2m
						c4emcol = 0xff1100
						c4coth = '<:c4yc:1130939019702837439>'
						c4intscol = c4intsr
					if c4p is c4p2:
						c4pmen = c4p2m
						c4poth = c4p1m
						c4emcol = 0xf6ff00
						c4coth = '<:c4rc:1130939020734636173>'
						c4intscol = c4intsy
					winind = f"**It's {c4poth.mention}'s turn!** {c4coth}"
					c4ffs = ["c4 ff", 'c4 forfeit', 'c4 q', 'c4 quit']
					rgc4 = None
					resp = '10'

					if not c4well == 0:
						while True:
							try:
								message = await bot.wait_for('message', check=lambda message: message.author == c4pmen, timeout=300)
								if message.content in c4ffs:
									await message.reply(f"**{c4pmen.mention} FORFEITED! {c4poth.mention} __WINS__!**")
									break
								elif not message.content in strints and message.content.isdigit():
									await message.reply(f"**__Try again, {c4pmen.mention}!__\nYour response wasn't a valid integer! You must respond with a number 1-7**")
								elif message.content in strints:
									resp = message.content
									for let in strabcs:
										if not resp in let:
											c4p.append(f"{rstrabcs[strabcs.index(let)]}{resp}")
											let.append(resp)
											rgc4 = True
											break
										if let == strabcs[-1]:
											await ctx.send(f"**__Try again, {c4pmen.mention}!__\nThe `{resp}` slot is full already!**")
							except asyncio.TimeoutError:
								norgc4 = [f"took too long to respond!","had to go run an errand rq.","didn't repsond.", "had an emergency.","broke the 5-minute threshold!"]
								await c4accmsg.reply(f"**{c4pmen.mention} {random.choice(norgc4)} __You win__ {c4poth.mention}!**")
								break
							if rgc4 is True:
								break
					if c4well == 0:
						winind = f"Welcome to **__Connect 4__!** \nIt's {c4poth.mention}'s turn!{board}"
						rgc4 = True
					if rgc4 is True:
						strabcsr = strabcs[::-1]
						lettind = -1
						c4NF = 0
						for lett in strabcsr:
							lettind+=1
							for q in range(1,8):
								if f"{rrstrabcs[lettind]}{q}" in c4p1:
									board+='<:c4red:1130933211216744550>'
								elif f"{rrstrabcs[lettind]}{q}" in c4p2:
									board+='<:c4yellow:1130933209190891551>'
								else:
									board+='<:c4empty:1130933212076572792>'
									c4NF+=1
							board+='\n'
							if lett is a and not resp is None:
								for c4inta in range(0,7):
									if c4inta+1 == int(resp):
										board+=c4intscol[c4inta]
									else:
										board+=c4intsem[c4inta]
							with open('c4e.txt','r+') as c4e:
								for ec in eval(c4e.read()):
									winint = 0
									for ecord in ec:
										if not ecord in c4p:
											winint-=1
									if winint == 0:
										winind = f"**You win {c4pmen.mention}!** :medal:"
										break
									if c4NF == 0 and not winint == 0:
										winind = f"**It's tied! :medal:**"
						c4boardembed = discord.Embed(title=f"{c4p1m.name} <:c4rc:1130939020734636173> VS {c4p2m.name} <:c4yc:1130939019702837439>", description=f"_ _\n{winind}\n\n{board}\n_ _", color=c4emcol, timestamp=ctx.message.created_at)
						await ctx.send(embed=c4boardembed)
						c4well+=1
						if winint == 0 or c4NF == 0:
							break
					if winint == 0 or rgc4 is None or c4NF == 0:
						break
				if winint == 0 or rgc4 is None or c4NF == 0:
					break


##### TEST COMMANDS #####

# @bot.command()
# async def randomwordletest(ctx):
# 	dictionary = PyDictionary()
# 	full = ""
# 	with open('words.txt','r+') as wordsraw:
# 		wordslist = eval(wordsraw.read())
# 		word = random.choice(wordslist)
# 		full += f"**__{word}__**\n\n"
# 		for a in dictionary.meaning(word):
# 			full += f"**{a}**\n"
# 			definition = 0
# 			for b in dictionary.meaning(word)[a]:
# 				definition +=1
# 				full+=(f"**{definition}:**  {b}\n")
# 			full += "\n"
# 	await ctx.send(full)




@bot.command()
@commands.cooldown(1,30,commands.BucketType.member)
async def intguess(ctx):
	igthread = await ctx.message.create_thread(name=f"{ctx.author.name} IntGuessr")
	await igthread.send(f"**{ctx.author.mention} Welcome to IntGeuss!** The game where you have **20** chances to guess the number I'm thinking of! (**out of `1,000,000`**)")
	await asyncio.sleep(3)
	igstart = await igthread.send("**`.......`**")
	for iga in range(1,6):
		await igstart.edit(content=f"**`{random.randint(0,1000000)}`**")
		await asyncio.sleep(0.5)
	await igstart.edit(content=f"**`.......`**")
	await asyncio.sleep(2)
	igans = random.randint(1,1000000)
	await igstart.edit(content="**I've got my number!** Try and guess it now!")
	await asyncio.sleep(2)
	await igstart.edit(content='**In 3....**')
	await asyncio.sleep(0.5)
	await igstart.edit(content='**2....**')
	await asyncio.sleep(0.5)
	await igstart.edit(content='**1...!**')
	await asyncio.sleep(0.5)
	await igstart.edit(content='**Start guessing 1-100! NOW!**')
	igtries = 0
	igwin = False
	for igturns in range(1,21):
		ignum = False
		while True:
			try:
				ctxguess = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
				if ctxguess.content.isdigit() and ctxguess.channel == igthread and int(ctxguess.content) <= 1000000:
					ignum = True
					break
			except asyncio.TimeoutError:
				await igthread.edit(name=f"{ctx.author.name} IntGuessr [Lost, Timed Out]", locked=True)
				await ctx.send(f"**60 second timeout has reached! The answer was `{igans}`! Game over! {ctx.author.mention}**")
				igwin = None
				break
		if ignum is True:
			if int(ctxguess.content) == igans:
				igwin = True
				igtries = igturns
				break
			if abs(igans-int(ctxguess.content)) <= 1000000:
				igresp = "Off the fucking grid."
			if abs(igans-int(ctxguess.content)) <= 750000:
				igresp = "Stone cold. (750k range)"
			if abs(igans-int(ctxguess.content)) <= 500000:
				igresp = "Cold. (500k range)"
			if abs(igans-int(ctxguess.content)) <= 300000:
				igresp = "Room temperature. (300k range)"
			if abs(igans-int(ctxguess.content)) <= 100000:
				igresp = "Warm. (100k range)"
			if abs(igans-int(ctxguess.content)) <= 50000:
				igresp = "Warmer.. (50k range)"
			if abs(igans-int(ctxguess.content)) <= 10000:
				igresp = "*Hot!* (10k range)"
			if abs(igans-int(ctxguess.content)) <= 5000:
				igresp = "*Hotter!* (5k range)"
			if abs(igans-int(ctxguess.content)) <= 1000:
				igresp = "*Steaming Hot!* (1k range)"
			if abs(igans-int(ctxguess.content)) <= 100:
				igresp = "*__BOILING HOT!__* (100 range)"
			if igans-int(ctxguess.content) < 0:
				igdirection = "Lower!"
			if igans-int(ctxguess.content) > 0:
				igdirection = "Higher!"
			await ctxguess.reply(f"**{igdirection}** [ **{igresp}** ] **`{20-igturns} attempts left.`**")
		if igwin is None:
			break
	if igwin is False:
		await igthread.edit(name=f"{ctx.author.name} IntGuessr [Lost]", locked=True)
		await igthread.send(f"**Sorry, the answer you were looking for was {igans}! You lose.**")
	if igwin is True:
		# with open('lvls.json','r+',encoding='utf-8') as levelsraw:

		await igthread.edit(name=f"{ctx.author.name} IntGuessr [Won in {igtries} attempts]", locked=True)
		await igthread.send(f"**You got it! The answer was `{igans}`! You win! `[Total attempts: {igtries}]`**")



@bot.command()
async def fourkay(ctx, gentext=None, member=None):
	image = Image.new(mode="RGB", size=(1920,540), color=(49,51,56))
	fontt = ImageFont.truetype('ggmed.ttf', 78)
	todayfont = ImageFont.truetype('ggmed.ttf', 52)
	genmem = ctx.author
	tip = ""
	if not member is None:
		if member.startswith('<@'):
			genmem = ctx.guild.get_member(int(re.search(r'\d+', member).group()))
		else:
			if not ctx.guild.get_member_named(member) is None:
				genmem = ctx.guild.get_member_named(member)
			else:
				tip = "**Tip: To include a message with spaces, add it in quotations.\nExample: `!fourkay \"hi, guys\" @person`**"
	
	genname = genmem.name
	if (genmem.nick):
		genname = genmem.nick
	if gentext is None:
		gentext = "Text unavailable"
	
	editable = ImageDraw.Draw(image)

	with requests.get(str(genmem.avatar)) as pfpurl:
		pfpurldata = pfpurl.content
	with open('pfp.png','wb') as pfp:
		pfp.write(pfpurldata)

	genpfp = Image.open('pfp.png')
	genpfp = genpfp.resize((200, 200))

	genmask = Image.new(mode="L", size=genpfp.size, color=0)
	genmaskd = ImageDraw.Draw(genmask)
	genmaskd.ellipse((0,0,200,200),fill=255)

	image.paste(im=genpfp, box=(200,170,400,370), mask=genmask)
	editable.text((480, 160), genname, fill=hex_to_rgb(str(genmem.color)), font=fontt)
	editable.text((480, 265), gentext, fill=(219,222,225), font=fontt, spacing=25)
	editable.text((editable.textlength(genname,font=fontt)+523,186), f"Today at {int(datetime.datetime.now().strftime('%I'))}{datetime.datetime.now().strftime(':%M %p')}", fill=(149, 155, 164), font=todayfont)
	image.save(f"Test.png")
	await ctx.send(content=tip,file=discord.File(f"Test.png"))

@bot.command()
async def mn(ctx,  member):
	print(ctx.guild.get_member_named(member))


@bot.command()
@commands.has_permissions(administrator=True)
async def embed(ctx):
	dembed = discord.Embed(title="**TITLE**", color=0x000000, type="rich", description="**DESCRIPTION**")
	dembed.set_author(name="**SET_AUTHOR NAME**", url="https://www.twitch.tv/kaicenat", icon_url="https://cdn.discordapp.com/attachments/919055834611347536/1071496444390953031/SET_AUTHOR_ICON_URL.png")
	dembed.add_field(name='**ADD_FIELD NAME**', value="**ADD_FIELD VALUE**")
	dembed.set_footer(text='**SET_FOOTER TEXT**', icon_url="https://cdn.discordapp.com/attachments/919055834611347536/1071494660553441471/TucsonPhysicalTherapy.png")
	dembed.set_image(url="https://cdn.discordapp.com/attachments/919055834611347536/1071493215036911798/SET_IMAGE.png")
	dembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/919055834611347536/1071493657888309290/SET_THUMBNAIL.png")
	await ctx.reply(embed=dembed)


##### ADMIN ######

# @bot.command()
# @commands.has_permissions(administrator=True)
# async def oy(ctx):
# 	y = 1
# 	o = 99999999999999999999999999999
# 	for member in ctx.guild.members:
# 		if member.bot is False:
# 			if member.id > y:
# 				y = member.id
# 			if member.id < o:
# 				o = member.id
# 	old = ctx.guild.get_member(o)
# 	young = ctx.guild.get_member(y)
# 	oldc = old.created_at
# 	youngc = young.created_at
# 	oldcr = oldc.strftime("%m-%d-20%y at %H:%M:%S")
# 	youngcr = youngc.strftime("%m-%d-20%y at %H:%M:%S")
# 	await ctx.reply(f"**The oldest account in this server is <@{o}> ! (Created {oldcr})\nThe youngest account is <@{y}> ! (Created {youngcr})**")

# @bot.command(aliases=["si","sinfo"])
# @commands.has_permissions(administrator=True)
# async def serverinfo(ctx):
# 	bots = 0
# 	admins = ""
# 	for member in ctx.guild.members:
# 		if member.bot is True:
# 			bots+=1
# 			print(member.mention)
# 		if member.guild_permissions.administrator is True and not member.id == 504072666718797836 and member.bot is False:
# 			admins += f"{member.mention}\n"

# 	emojis = ""
# 	aniemojis = ""
# 	emojisint = 0
# 	aniemojisint = 0
# 	for emo in ctx.guild.emojis:
# 		if emo.animated is False:
# 			emojisint += 1
# 		if emo.animated is True:
# 			aniemojisint += 1
# 	for emoji in ctx.guild.emojis:
# 		if emoji.animated is False:
# 			emojis += f"<:{emoji.name}:{emoji.id}> "
# 		if emoji.name == "itemAndesite" or len(emojis) > 969:
# 			emojis += "**etc..**"
# 			break
# 	for aniemoji in ctx.guild.emojis:
# 		if aniemoji.animated is True:
# 			aniemojis += f"<a:{aniemoji.name}:{aniemoji.id}> "
# 		if len(aniemojis) > 969:
# 			aniemojis += "**etc..**"
# 			break
# 	van = "**[`No Vanity URL`]**"
# 	if not ctx.guild.vanity_url_code is None:
# 		van = f"**[`discord.gg/{ctx.guild.vanity_url_code}`]**"
# 	tchan = ""
# 	if len(ctx.guild.text_channels) > 0:
# 		tchan = f"ㅤ`{len(ctx.guild.text_channels)}` Text Channels\n"
# 	vchan = ""
# 	if len(ctx.guild.voice_channels) > 0:
# 		vchan = f"ㅤ`{len(ctx.guild.voice_channels)}` Voice Channels [`{round(ctx.guild.bitrate_limit/1000)}kbps BR`]\n"
# 	thchan = ""
# 	if len(ctx.guild.threads) > 0:
# 		thchan = f"ㅤ`{len(ctx.guild.threads)}` Threads\n"
# 	schan = ""
# 	if len(ctx.guild.stage_channels) > 0:
# 		schan = f"ㅤ`{len(ctx.guild.stage_channels)}` Stage Channels\n"
# 	fchan = ""
# 	if len(ctx.guild.forums) > 0:
# 		fchan = f"ㅤ`{len(ctx.guild.forums)}` Forums\n"
# 	nboosts = "**`No Boosts Yet!`**\n"
# 	tboosts = ""
# 	bboosts = ""
# 	f"Boosters Count - {ctx.guild.premium_subscription_count}\nBoosting Tier - {ctx.guild.premium_tier}\nBooster Bar - {ctx.guild.premium_progress_bar_enabled}\n"
# 	if ctx.guild.premium_subscription_count > 0:
# 		nboosts = f"**`{ctx.guild.premium_subscription_count}` Server Boosts**\n"
# 		tboosts = f"**`{2-ctx.guild.premium_subscription_count} Boosts` left until `Level 1`**\n"
# 		if ctx.guild.premium_tier == 1:
# 			tboosts = f"**`Level 1` [`{7-ctx.guild.premium_subscription_count} Boosts` left until `Level 2`]**\n"
# 		if ctx.guild.premium_tier == 2:
# 			tboosts = f"**`Level 2` [`{14-ctx.guild.premium_subscription_count} Boosts` left until `Level 3`]**\n"
# 		if ctx.guild.premium_tier == 3:
# 			tboosts = f"**`Level 3` [__MAX!__]**\n"
# 	if ctx.guild.premium_progress_bar_enabled is True:
# 		bboosts = "*** Progress Bar Enabled**\n"
# 	ctx.guild.stage_instances, ctx.guild.scheduled_events, ctx.guild.banner, ctx.guild.created_at
# 	ctx.guild.premium_subscribers
# 	insend = discord.Embed(color=0x000000, title=f"{ctx.guild.name}\n{ctx.guild.description}\n{van}", description=
# 	f"**__Owner:__**\n<@{ctx.guild.owner_id}>\n\n**__Admins:__**\n{admins}\n**`{ctx.guild.member_count}` Members [`{round(ctx.guild.max_members/1000)}k Max`]\nㅤ**`{len(ctx.guild.members)-bots}` Humans**\nㅤ**`{bots}` Bots**\n\n`{len(ctx.guild.channels)-len(ctx.guild.categories)}` Channels [`{len(ctx.guild.categories)} Cat.`]\n{tchan}{vchan}{thchan}{schan}{fchan}\n`{round(ctx.guild.filesize_limit/1048576)}MB` Filesize Limit [No Nitro]**\n\n{nboosts}{tboosts}{bboosts}\n\nVerification Level: {str(ctx.guild.verification_level).upper()}\nDefault Notifs - {ctx.guild.default_notifications}")
# 	insend.set_author(name="Server Information!", icon_url='https://cdn.discordapp.com/emojis/1015818267358679070.webp?size=96&quality=lossless')
# 	insend.add_field(name=f"{emojisint} Emotes   (LImit: {ctx.guild.emoji_limit})", value=emojis)
# 	insend.add_field(name=f"{aniemojisint} Animated Emotes   (Limit: {ctx.guild.sticker_limit})", value=aniemojis)
# 	insend.set_footer(text=f"")
# 	insend.set_thumbnail(url=ctx.guild.icon)
# 	if not ctx.guild.banner is None:
# 		insend.set_image(url=ctx.guild.banner)
# 	await ctx.send(embed=insend)

# @bot.command(aliases=['mi','minfo','userinfo','uinfo','who','whois','w'])
# @commands.has_permissions(administrator=True)
# async def memberinfo(ctx, member:discord.Member):
# 	memroles = ""
# 	for roles in member.roles:
# 		role = ctx.guild.get_role(roles.id)
# 		crown = ""
# 		if role.mention == member.top_role.mention:
# 			crown = ":crown:"
# 		memroles += f"{role.mention} {crown}\n"
# 	created_at = member.created_at
# 	hr = int(created_at.strftime('%H'))
# 	if hr > 12:
# 		memcreation = created_at.strftime(f'**{hr-12}**:**%M**:**%S** **PM** **%m**/**%d**/**%y**')
# 	else:
# 		memcreation = created_at.strftime(f'**{hr}**:**%M**:**%S** **AM** **%m**/**%d**/**%y**')
# 	joined_at = member.joined_at
# 	hr = int(joined_at.strftime('%H'))
# 	if hr > 12:
# 		memjoined = joined_at.strftime(f'**{hr-12}**:**%M**:**%S** **PM** **%m**/**%d**/**%y**')
# 	else:
# 		memjoined = joined_at.strftime(f'**{hr}**:**%M**:**%S** **AM** **%m**/**%d**/**%y**')
# 	mutualgs = ""
# 	for m in member.mutual_guilds:
# 		mutualgs += f"\n**{m.name}**, {m.member_count} members"
# 	sen = discord.Embed(color=0x000000, title="ugh", description='')
# 	sen.add_field(name='Obvious',value=f'**Name (user’s username) -** {member.name}\n**Mention (mention the member) -** {member.mention}\n**Nickname (guild specific nickname of the user) -** {member.nick}\n**Display Name (ser’s server nick) -** {member.display_name}\n**Discriminator (user’s discriminator) -** {member.discriminator}\n**Member ID (The user’s unique ID.) -** {member.id}\n')
# 	sen.add_field(name='Profiles',value=f'**Avatar -** {member.avatar}\n**Display Avatar (member’s server pfp) -** {member.display_avatar}\n**Def Avatar (the default avatar for a given user) -** {member.default_avatar}\n**Banner (user banner) -** {member.banner}\n**Accent Color (def banner color) -** {member.accent_color}\n', inline=False)
# 	sen.add_field(name='Status',value=f'**Activites (user is currently doing) -** {member.activities}\n**Activity (what user is currently doing) -** {member.activity}\n**Status (member’s overall status) -** {member.status}\n**Raw Status (member’s overall status as a string value) -** {member.raw_status}\n**Desktop Status (member’s status on the desktop client) -** {member.desktop_status}\n**Mobile Status (member’s status on a mobile device) -** {member.mobile_status}\n**Web Status (member’s status on the web client) -** {member.web_status}', inline=False)
# 	sen.add_field(name='Acc Is:',value=f'**Bot (if the user is a bot account) -** {member.bot}\n**Pending (Whether the member is pending member verification) -** {member.pending}\n**Mutual Guilds (guilds that the user shares with the client.) -** {mutualgs}\n**System (if the user is a system user, represents Discord officially) -** {member.system}\n**Public Flags (publicly available flags the user has) -** {member.public_flags.value}\n**Voice (the member’s current voice state) -** {member.voice}\n**Resolved Permissions (the member’s resolved permissions from an interaction) -** {member.resolved_permissions}\n', inline=False)
# 	sen.add_field(name='Guild-Chosen',value=f'**Guild (guild that the member belongs to) -** {member.guild}\n**Color (a color denoting the rendered color for the member) -** {member.color}\n**Display Icon (the role icon that is rendered for this member) -** {member.display_icon}\n**Roles (A list of Role that the member belongs to) -** {memroles}\n**Guild Permissions (the member’s guild permissions) -** {member.guild_permissions.value}\n', inline=False)
# 	sen.add_field(name='Dates',value=f'**Created Date -** {memcreation}\n**Joined At -** {memjoined}\n**Premium Since (datetime object that specifies the date and time in UTC when the member used their “Nitro boost” on the guild) -** {member.premium_since}\n**Timed Out Until (datetime object that specifies the date and time in UTC that the member’s time out will expire) -** {member.timed_out_until}\n', inline=False)
# 	await ctx.send(embed=sen)

# @bot.command(aliases=["ri","rinfo"])
# @commands.has_permissions(administrator=True)
# async def roleinfo(ctx):
# 	for role in ctx.guild.roles:
# 		if role.id == 816855204803641365:
# 			for a in role.members:
# 				print(a.name)

cogs = [
	res.Res(bot),
	mod.StaffCommands(bot),
]

async def setup():
	for cog in cogs:
		await bot.add_cog(cog)
asyncio.run(setup())


with open("t.0", "r", encoding="utf-8") as f:
	token = f.read()

bot.run(token)