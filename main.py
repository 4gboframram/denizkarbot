import discord
import os
import requests
import json
import random
import asyncio
from requests.exceptions import RequestException
client = discord.Client()
intents = discord.Intents.default()
intents.members = True
from levels2 import levels, xps, update_xp
#Sad Words
sad_words = [
	"sad",
	"depressed",
	"unhappy",
]

#Replies to sad words
starter_encouragements = [
	"Cheer up!",
	"Hang in there.",
	"You're too cute to be sad =}",
	"I don't want to see you sad :(",
]

#coin flip options
coinflip = ["Heads", "Tails"]

from discord.ext import commands
bot = commands.Bot(command_prefix='!den ')


@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="All my Cuties :3"))


@bot.event
async def on_message(message):
	sadge='sadge'
	h = 'h', 'H', 'н'
	msg = message.content
	gn = 'gn ', 'Gn ', 'gn!'
	gn2='gn', 'Gn'
	gn3='agn', 'ign', 'egn', 'ogn', 'ugn'
	if message.author == bot.user:
		return
	if any(word in msg for word in sad_words):	#detect sad words
		if msg in sadge:
			await message.channel.send('sadge')
			return
		else: 
			await message.channel.send(random.choice(starter_encouragements))	#send encouragements
	if msg in h:	#detect h
		await message.channel.send(random.choice(h))	#send h
	await bot.process_commands(message)
	if any(word in msg for word in gn):	#detect gn
		if any(word in msg for word in gn3):
			return
		await message.channel.send('Sleepy well, cutie! :3')	#send h
	if msg in gn2:
		await message.channel.send('Sleepy well, cutie! :3')
	if message.content.startswith('```'):
		if message.author.guild_permissions.administrator: 
			return
		else: 
			await message.delete()
			embed=discord.Embed(title="Stop", description=f"{message.author.mention}, stop abusing syntax highlighting please. It's not funny.", colour=0xff0000)	
			embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
			await message.channel.send(embed=embed)	
	userid=message.author.id
	update_xp(userid).gain().save()
	if update_xp(userid).xp>= xps(update_xp(userid).level+1):
		update_xp(userid).setxp(0)
		update_xp(userid).increaselvl(1)
		embed=discord.Embed(title="Level Up?", description=f"{message.author.mention}, you have leveled up to level {levels.dict[str(userid)][1]}. Poggies <3", colour=0xffbbcc)	
		embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
		await message.channel.send(embed=embed)	


@bot.event
async def on_command_error(ctx, error):
		# if command has local error handler, return
		if hasattr(ctx.command, 'on_error'):
			return

		# get the original exception
		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			embed = discord.Embed(title="Oops",description="Command does not exist.\n ", colour=0xff0000)
			embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
			embed.add_field(name='Technical details', value='Error: `commands.CommandNotFound`')
			await ctx.send(embed=embed)
			return

		if isinstance(error, commands.BotMissingPermissions):
			missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
			if len(missing) > 2:
				fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
			else:
				fmt = ' and '.join(missing)
			_message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
			embed = discord.Embed(title="Oops",description=_message, colour=0xff0000)
			embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
			embed.add_field(name='Technical details:', value='Error: `commands.BotMissingPermissions`')
			await ctx.send(embed=embed)
			return

		if isinstance(error, commands.DisabledCommand):
			await ctx.send('This command has been disabled.')
			return

		if isinstance(error, commands.MissingPermissions):
			missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
			if len(missing) > 2:
				fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
			else:
				fmt = ' and '.join(missing)
			_message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
			embed = discord.Embed(title="Oops",description=_message, colour=0xff0000)
			embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
			embed.add_field(name='Technical details:', value='Error: `commands.MissingPermissions`')
			await ctx.send(embed=embed)
			return

		if isinstance(error, commands.NoPrivateMessage):
			try:
				await ctx.author.send('This command cannot be used in direct messages.')
			except discord.Forbidden:
				pass
			return

		if isinstance(error, commands.CheckFailure):
			embed = discord.Embed(title="Oops",description="You do not have permission to use this command.", colour=0xff0000)
			embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
			embed.add_field(name='Technical details:', value='Error: `commands.CheckFailure`')
			await ctx.send(embed=embed)
			return

@bot.command(name='unsad',
			 help='use this when you\'re sad =}',
			 Category='Cheerful')
async def unsad(ctx):
	def get_quote():
		response = requests.get("https://zenquotes.io/api/random")
		json_data = json.loads(response.text)
		quote = json_data[0]['q'] + " -" + json_data[0]['a']
		return (quote)

	quote = get_quote()
	embed = discord.Embed(title="Hope this helps!",description=quote, colour=discord.Colour.magenta())
	await ctx.send(embed=embed)


@bot.command(name='ram',
			 help='you\'ll find out what this does if you use it',
			 Category='Fun')
async def ram(ctx):
	embed = discord.Embed(title='Ram best girl',description='Ram is best girl, but we all know that I am second best =}', colour=discord.Colour.magenta())
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await ctx.send(embed=embed)


@bot.command(name='coin', help='flip a coin', Category='Utility')
async def coin(ctx):
	embed = discord.Embed(title='Coin Flip Results',description=random.choice(coinflip), colour=discord.Colour.magenta())
	await ctx.send(embed=embed)

@bot.command(name='rolecreate', help='create a role with a hex color')
@commands.has_permissions(manage_roles=True)
async def rolecreate(ctx, name, color):
	print('command started')
	guild = ctx.guild
	colorhex = int(color, 16)
	await guild.create_role(name=name, color=discord.Colour(colorhex))
	await ctx.send(f'Role `{name}` has been created""')


@bot.command(name="makesad",
			 help="sends an ai-generated quote to probably make you sadn't")
async def makesad(ctx):

	# sends GET request to Inspirobot for image url response
	try:
		url = 'http://inspirobot.me/api?generate=true'
		params = {'generate': 'true'}
		response = requests.get(url, params, timeout=10)
		image = response.text
		embed=discord.Embed(title='Sorry I\'m doing my best :(', colour=discord.Colour.magenta())
		embed.set_image(url=image)
		embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
		await ctx.send(embed=embed)

	except RequestException:

		await ctx.send('Inspirobot is broken, there is no reason to live.')


#The below code bans player.
@bot.command(help='you know')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	if member.guild_permissions.manage_messages:
		embed = discord.Embed(title="Oops",description="You do not have the permission to ban that user", colour=0xff0000)
		embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
		await ctx.send(embed=embed)
		return ('a')
	await member.ban(reason=reason)
	embed = discord.Embed(title="Banned",description=f"You {member.mention} has been banned :(", colour=0xff0000)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await ctx.send(f'{member} has been banned \nReason: {reason}')


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")
	if member.guild_permissions.manage_messages:
		embed = discord.Embed(title="Oops",description="You do not have the permission to mute that user", colour=0xff0000)
		embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
		await ctx.send(embed=embed)
		return
	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole,
											speak=False,
											send_messages=False,
											read_message_history=True,
											read_messages=True)
	embed = discord.Embed(title="muted",
							description=f"{member.mention} was muted ",
							colour=0xfff200)
	embed.add_field(name="reason:", value=reason, inline=False)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	
	await ctx.send(embed=embed)
	await member.add_roles(mutedRole, reason=reason)
	await member.send(
		f" you have been muted from: {guild.name} reason: {reason}")


@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
	await member.remove_roles(mutedRole)
	await member.send(f" you have unmuted from: - {ctx.guild.name}")
	embed = discord.Embed(title="unmute",
							description=f" unmuted-{member.mention}",
							colour=discord.Colour.green())
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
	if member.guild_permissions.manage_messages:
		embed = discord.Embed(title="Oops",description="You do not have the permission to mute that user", colour=discord.Colour.red())
		embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatarmutes/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
		await ctx.send(embed=embed)
		return
	guild = ctx.guild

	for role in guild.roles:
		if role.name == "Muted":
			await member.add_roles(role)

			embed = discord.Embed(
				title="muted!",
				description=f"{member.mention} has been tempmuted ",
				colour=0xfff200)
			embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')	
			embed.add_field(name="reason:", value=reason, inline=False)
			embed.add_field(name="time left for the mute:",
							value=f"{time}{d}",
							inline=False)
			await ctx.send(embed=embed)

			if d == "s":
				await asyncio.sleep(time)

			if d == "m":
				await asyncio.sleep(time * 60)

			if d == "h":
				await asyncio.sleep(time * 60 * 60)

			if d == "d":
				await asyncio.sleep(time * 60 * 60 * 24)

			await member.remove_roles(role)

			embed = discord.Embed(title="unmute (temp) ",
									description=f"unmuted -{member.mention} ",
									colour=0x00ff00)
			await ctx.send(embed=embed)

			return

@bot.command(name='lock')
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel, *, reason=None):
	if reason==None:
		r='Unspecified'	
	else:
		r=reason
	await channel.set_permissions(ctx.guild.default_role, send_messages=False)
	embed = discord.Embed(title="Channel Locked",description=f"{ctx.author.mention} has locked this channel, {channel.mention}\nReason: {r}", colour=0xffff00)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await channel.send(embed=embed)



@bot.command(name='unlock')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel,*, reason=None):
	if reason==None:
		r='Unspecified'
	else:
		r=reason
	await channel.set_permissions(ctx.guild.default_role, send_messages=True)
	embed = discord.Embed(title="Channel Unlocked",description=f"{ctx.author.mention} has unlocked this channel, {channel.mention}\nReason: {r}", colour=0xffff00)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await channel.send(embed=embed)

@bot.command(name='percent')
async def p(ctx, something):
	h=hash(str(ctx.author.id)+f' {something}')
	embed=discord.Embed(title='Rate',description=f"{ctx.author.mention}, you are {h%101}% {something}",colour=0xcc00ff)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')	
	await ctx.send(embed=embed)

@bot.command(name='rate')
async def rate(ctx, thing):
	if thing=='Ram' or thing=='ram' or thing=='denizkar' or thing=='Denizkar' or thing=='den' or thing=='Den': randint=11
	else: randint=hash(thing)%11
	if randint==8 or randint==11: article='an'
	else: article='a'
	embed=discord.Embed(title='Rate',description=f"I'd rate *{thing}* {article} {randint} out of 10",colour=0xcc00ff)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')	
	await ctx.send(embed=embed)

@bot.command() 
@commands.has_permissions(administrator=True)
async def send(ctx, message):
	for guild in bot.guilds:
		await ctx.send(guild)
		embed=discord.Embed(title=f"Announcement from {ctx.author}, in {ctx.guild}", description=f"{message}",colour=0x666a66)
		await guild.text_channels[0].send(embed=embed)
@bot.command(name='status')
@commands.has_permissions(administrator=True)
async def status(ctx,type_,status):
	embed=discord.Embed(title="Bot Status Changed", description=f"Denizkar Bot is now {type_} {status}", colour=0xadfea)	
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')	
	if type_=='playing':
		await bot.change_presence(activity=discord.Game(name=status))
		await ctx.send(embed=embed)
	if type_=='streaming':
		await bot.change_presence(activity=discord.Streaming(name=status, url='https://discordpy.readthedocs.io/'))
		await ctx.send(embed=embed)
	if type_=='listening':
		await bot.change_presence(activity=discord.Listening(name=status))
		await ctx.send(embed=embed)
	if type_=='watching': 
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
		await ctx.send(embed=embed)

@bot.command(name='half')
async def half(ctx):
	f=open('halfpercent.txt','r')
	seeds=f.readlines()
	seed=random.choice(seeds)
	embed=discord.Embed(title="Half%", description=f"Here is your half% practice seed: {seed}", colour=0xddeffc, url='https://www.youtube.com/watch?v=FtutLA63Cp8')	
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await ctx.send(embed=embed)

@bot.command(name='alllogs')
async def alllogs(ctx):
	embed=discord.Embed(title="Logs%", description="You don't need a practice seed lol. The rsg is dead", colour=0xddeffc,)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await ctx.send(embed=embed)

@bot.command()
async def fsg(ctx):
	embed=discord.Embed(title="fsg%", description='Just use the normal seed finder', colour=0xddeffc, url="https://repl.it/@AndyNovo/filteredseed")
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')
	await ctx.send(embed=embed)
@bot.command()
async def blue(ctx,message):
	await ctx.send(f'```py \n\'{message}\'\n```')


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())



@bot.command()
async def xp(ctx):
	embed=discord.Embed(title='Level?',description=f"{ctx.author.mention}, you are level {update_xp(ctx.author.id).level}.\n You are {xps(update_xp(ctx.author.id).level+1)- update_xp(ctx.author.id).xp} away from leveling up to level {update_xp(ctx.author.id).level+1}",colour=0xcc00ff)
	embed.set_author(name="Denizkar Bot", icon_url='https://cdn.discordapp.com/avatars/814549074938298370/449eec7e1b99f5bdf44992b2d8afe38a.webp?size=2048')	
	await ctx.send(embed=embed)
		



from keep_alive import keep_alive
keep_alive()
bot.run(os.getenv('TOKEN'))
	
