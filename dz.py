import discord
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
from datetime import datetime

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
	print(f"\n{bot.user.name}!\n")
	stream = discord.Streaming(name='Strawberry Sky By dz!', url='https://www.youtube.com/watch?v=i5Xmk-ciobo', platform='YouTube')
	gen = bot.get_channel(1070872824685789266)
	await bot.change_presence(activity=stream)
	await gen.send("on")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		msg = '**This command is still on cooldown for another __{:.2f} seconds__!**'.format(error.retry_after)
		await ctx.send(msg)
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("**Error: `That command does not exist.`**")
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Error: `You are missing a part of your command.`**") 
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("**Error: `That is an ADMIN command!`**")
	if isinstance(error, commands.errors.ChannelNotFound):
		await ctx.send("**Error: `That channel doesn't exist.`**")
	if isinstance(error, commands.errors.RoleNotFound):
		await ctx.send("**Error: `Couldn't find role.`**")
	if isinstance(error, commands.errors.TooManyArguments):
		await ctx.send(f"**Error: `Unwanted details in command. ({error.args})`**")
	if isinstance(error, commands.errors.UserNotFound):
		await ctx.send("**Error: `Couldn't find member.`**")
	print(error)

@bot.command()
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
	if 1009 < pin:
		status = "Something is terribly wrong."
	await ctx.reply(f'**{round(bot.latency * 1000)}ms (`{status}`)**')
	await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def any(ctx):
	vc = ctx.guild.get_channel(921039464934039583)
	await vc.connect()
	


@bot.command()
@commands.has_permissions(administrator=True)
async def oy(ctx):
	y = 1
	o = 99999999999999999999999999999
	for member in ctx.guild.members:
		if member.bot is False:
			if member.id > y:
				y = member.id
			if member.id < o:
				o = member.id
	old = ctx.guild.get_member(o)
	young = ctx.guild.get_member(y)

	oldc = old.created_at
	youngc = young.created_at

	oldcr = oldc.strftime("%m-%d-20%y at %H:%M:%S")
	youngcr = youngc.strftime("%m-%d-20%y at %H:%M:%S")

	await ctx.reply(f"**The oldest account in this server is <@{o}> ! (Created {oldcr})\nThe youngest account is <@{y}> ! (Created {youngcr})**")
	print("done")


# @bot.command()
# async def ahh(ctx):
# 	channel = discord.utils.get(ctx.guild.channels, name='dz')
# 	headers = {'authorization': 'NTA0MDcyNjY2NzE4Nzk3ODM2.GgMufU.rYZmlpheIVCSv1ONAWban3tr8pVesIbAyW9a2s'}
# 	full = []
# 	for textchannel in ctx.guild.text_channels:
# 		print(textchannel.name)
# 		r = requests.get(f'https://discord.com/api/v9/channels/{textchannel.id}/messages', headers=headers)
# 		jsonn = json.loads(r.text)
# 		for msg in jsonn:
# 			if msg['author']['id'] == '690835715009019944' and not msg['content'].startswith("!"):
# 				full.append(msg['content'])
# 				len(full)
# 	poll = 0
# 	polly = 5
# 	mean = ""
# 	polled = 0
# 	nice = ""
# 	for mess in full:
# 		text = TextBlob(mess)
# 		pol = round(3+(text.sentiment.polarity*2),1)
# 		poll += pol
# 		if pol < polly:
# 			polly = pol
# 			mean = mess
# 		if pol > polled:
# 			polled = pol
# 			nice = mess
# 	print(f"{round(poll/len(full),1)} score out of {len(full)} msgs.")
# 	print(f"Here's the meanest msg: {mean} ({polly})\nAnd here's the nicest one: {nice} ({polled})")


@bot.command(aliases=["si","sinfo"])
@commands.has_permissions(administrator=True)
async def serverinfo(ctx):
	bots = 0
	admins = ""
	for member in ctx.guild.members:
		if member.bot is True:
			bots+=1
			print(member.mention)
		if member.guild_permissions.administrator is True and not member.id == 504072666718797836 and member.bot is False:
			admins += f"{member.mention}\n"

	emojis = ""
	aniemojis = ""
	emojisint = 0
	aniemojisint = 0
	for emo in ctx.guild.emojis:
		if emo.animated is False:
			emojisint += 1
		if emo.animated is True:
			aniemojisint += 1
	for emoji in ctx.guild.emojis:
		if emoji.animated is False:
			emojis += f"<:{emoji.name}:{emoji.id}> "

		if emoji.name == "itemAndesite" or len(emojis) > 969:
			emojis += "**etc..**"
			break
	for aniemoji in ctx.guild.emojis:
		if aniemoji.animated is True:
			aniemojis += f"<a:{aniemoji.name}:{aniemoji.id}> "
		if len(aniemojis) > 969:
			aniemojis += "**etc..**"
			break
	
	van = "**[`No Vanity URL`]**"
	if not ctx.guild.vanity_url_code is None:
		van = f"**[`discord.gg/{ctx.guild.vanity_url_code}`]**"

	tchan = ""
	if len(ctx.guild.text_channels) > 0:
		tchan = f"ㅤ`{len(ctx.guild.text_channels)}` Text Channels\n"
	vchan = ""
	if len(ctx.guild.voice_channels) > 0:
		vchan = f"ㅤ`{len(ctx.guild.voice_channels)}` Voice Channels [`{round(ctx.guild.bitrate_limit/1000)}kbps BR`]\n"
	thchan = ""
	if len(ctx.guild.threads) > 0:
		thchan = f"ㅤ`{len(ctx.guild.threads)}` Threads\n"
	schan = ""
	if len(ctx.guild.stage_channels) > 0:
		schan = f"ㅤ`{len(ctx.guild.stage_channels)}` Stage Channels\n"
	fchan = ""
	if len(ctx.guild.forums) > 0:
		fchan = f"ㅤ`{len(ctx.guild.forums)}` Forums\n"

	nboosts = "**`No Boosts Yet!`**\n"
	tboosts = ""
	bboosts = ""
	f"Boosters Count - {ctx.guild.premium_subscription_count}\nBoosting Tier - {ctx.guild.premium_tier}\nBooster Bar - {ctx.guild.premium_progress_bar_enabled}\n"
	if ctx.guild.premium_subscription_count > 0:
		nboosts = f"**`{ctx.guild.premium_subscription_count}` Server Boosts**\n"
		tboosts = f"**`{2-ctx.guild.premium_subscription_count} Boosts` left until `Level 1`**\n"
		if ctx.guild.premium_tier == 1:
			tboosts = f"**`Level 1` [`{7-ctx.guild.premium_subscription_count} Boosts` left until `Level 2`]**\n"
		if ctx.guild.premium_tier == 2:
			tboosts = f"**`Level 2` [`{14-ctx.guild.premium_subscription_count} Boosts` left until `Level 3`]**\n"
		if ctx.guild.premium_tier == 3:
			tboosts = f"**`Level 3` [__MAX!__]**\n"
	if ctx.guild.premium_progress_bar_enabled is True:
		bboosts = "*** Progress Bar Enabled**\n"
		

	ctx.guild.stage_instances, ctx.guild.scheduled_events, ctx.guild.banner, ctx.guild.created_at
	ctx.guild.premium_subscribers


	insend = discord.Embed(color=0x000000, title=f"{ctx.guild.name}\n{ctx.guild.description}\n{van}", description=
	f"**__Owner:__**\n<@{ctx.guild.owner_id}>\n\n**__Admins:__**\n{admins}\n**`{ctx.guild.member_count}` Members [`{round(ctx.guild.max_members/1000)}k Max`]\nㅤ**`{len(ctx.guild.members)-bots}` Humans**\nㅤ**`{bots}` Bots**\n\n`{len(ctx.guild.channels)-len(ctx.guild.categories)}` Channels [`{len(ctx.guild.categories)} Cat.`]\n{tchan}{vchan}{thchan}{schan}{fchan}\n`{round(ctx.guild.filesize_limit/1048576)}MB` Filesize Limit [No Nitro]**\n\n{nboosts}{tboosts}{bboosts}\n\nVerification Level: {str(ctx.guild.verification_level).upper()}\nDefault Notifs - {ctx.guild.default_notifications}")
	insend.set_author(name="Server Information!", icon_url='https://cdn.discordapp.com/emojis/1015818267358679070.webp?size=96&quality=lossless')

	insend.add_field(name=f"{emojisint} Emotes   (LImit: {ctx.guild.emoji_limit})", value=emojis)
	insend.add_field(name=f"{aniemojisint} Animated Emotes   (Limit: {ctx.guild.sticker_limit})", value=aniemojis)
	insend.set_footer(text=f"")
	insend.set_thumbnail(url=ctx.guild.icon)
	if not ctx.guild.banner is None:
		insend.set_image(url=ctx.guild.banner)
	await ctx.send(embed=insend)


@bot.command()
async def embed(ctx):
	dembed = discord.Embed(title="**TITLE**", color=0x000000, type="rich", description="**DESCRIPTION**")
	dembed.set_author(name="**SET_AUTHOR NAME**", url="https://www.twitch.tv/kaicenat", icon_url="https://cdn.discordapp.com/attachments/919055834611347536/1071496444390953031/SET_AUTHOR_ICON_URL.png")
	dembed.add_field(name='**ADD_FIELD NAME**', value="**ADD_FIELD VALUE**")
	dembed.set_footer(text='**SET_FOOTER TEXT**', icon_url="https://cdn.discordapp.com/attachments/919055834611347536/1071494660553441471/TucsonPhysicalTherapy.png")
	dembed.set_image(url="https://cdn.discordapp.com/attachments/919055834611347536/1071493215036911798/SET_IMAGE.png")
	dembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/919055834611347536/1071493657888309290/SET_THUMBNAIL.png")
	await ctx.reply(embed=dembed)



@bot.command(aliases=['mi','minfo','userinfo','uinfo','who','whois','w'])
async def memberinfo(ctx, member:discord.Member):
	memroles = ""
	for roles in member.roles:
		role = ctx.guild.get_role(roles.id)
		crown = ""
		if role.mention == member.top_role.mention:
			crown = ":crown:"
		memroles += f"{role.mention} {crown}\n"
	
	created_at = member.created_at
	hr = int(created_at.strftime('%H'))
	if hr > 12:
		memcreation = created_at.strftime(f'**{hr-12}**:**%M**:**%S** **PM** **%m**/**%d**/**%y**')
	else:
		memcreation = created_at.strftime(f'**{hr}**:**%M**:**%S** **AM** **%m**/**%d**/**%y**')
	joined_at = member.joined_at
	hr = int(joined_at.strftime('%H'))
	if hr > 12:
		memjoined = joined_at.strftime(f'**{hr-12}**:**%M**:**%S** **PM** **%m**/**%d**/**%y**')
	else:
		memjoined = joined_at.strftime(f'**{hr}**:**%M**:**%S** **AM** **%m**/**%d**/**%y**')
	
	mutualgs = ""
	for m in member.mutual_guilds:
		mutualgs += f"\n**{m.name}**, {m.member_count} members"
	sen = discord.Embed(color=0x000000, title="ugh", description='')
	sen.add_field(name='Obvious',value=f'**Name (user’s username) -** {member.name}\n**Mention (mention the member) -** {member.mention}\n**Nickname (guild specific nickname of the user) -** {member.nick}\n**Display Name (ser’s server nick) -** {member.display_name}\n**Discriminator (user’s discriminator) -** {member.discriminator}\n**Member ID (The user’s unique ID.) -** {member.id}\n')
	sen.add_field(name='Profiles',value=f'**Avatar -** {member.avatar}\n**Display Avatar (member’s server pfp) -** {member.display_avatar}\n**Def Avatar (the default avatar for a given user) -** {member.default_avatar}\n**Banner (user banner) -** {member.banner}\n**Accent Color (def banner color) -** {member.accent_color}\n', inline=False)
	sen.add_field(name='Status',value=f'**Activites (user is currently doing) -** {member.activities}\n**Activity (what user is currently doing) -** {member.activity}\n**Status (member’s overall status) -** {member.status}\n**Raw Status (member’s overall status as a string value) -** {member.raw_status}\n**Desktop Status (member’s status on the desktop client) -** {member.desktop_status}\n**Mobile Status (member’s status on a mobile device) -** {member.mobile_status}\n**Web Status (member’s status on the web client) -** {member.web_status}', inline=False)
	sen.add_field(name='Acc Is:',value=f'**Bot (if the user is a bot account) -** {member.bot}\n**Pending (Whether the member is pending member verification) -** {member.pending}\n**Mutual Guilds (guilds that the user shares with the client.) -** {mutualgs}\n**System (if the user is a system user, represents Discord officially) -** {member.system}\n**Public Flags (publicly available flags the user has) -** {member.public_flags.value}\n**Voice (the member’s current voice state) -** {member.voice}\n**Resolved Permissions (the member’s resolved permissions from an interaction) -** {member.resolved_permissions}\n', inline=False)
	sen.add_field(name='Guild-Chosen',value=f'**Guild (guild that the member belongs to) -** {member.guild}\n**Color (a color denoting the rendered color for the member) -** {member.color}\n**Display Icon (the role icon that is rendered for this member) -** {member.display_icon}\n**Roles (A list of Role that the member belongs to) -** {memroles}\n**Guild Permissions (the member’s guild permissions) -** {member.guild_permissions.value}\n', inline=False)
	sen.add_field(name='Dates',value=f'**Created Date -** {memcreation}\n**Joined At -** {memjoined}\n**Premium Since (datetime object that specifies the date and time in UTC when the member used their “Nitro boost” on the guild) -** {member.premium_since}\n**Timed Out Until (datetime object that specifies the date and time in UTC that the member’s time out will expire) -** {member.timed_out_until}\n', inline=False)
	await ctx.send(embed=sen)

@bot.command(aliases=["ri","rinfo"])
async def roleinfo(ctx):
	for role in ctx.guild.roles:
		if role.id == 816855204803641365:
			for a in role.members:
				print(a.name)

cogs = [
	res.Res(bot),
	mod.StaffCommands(bot)
]

async def setup():
	for cog in cogs:
		await bot.add_cog(cog)
asyncio.run(setup())


with open("t.0", "r", encoding="utf-8") as f:
	token = f.read()

bot.run(token)