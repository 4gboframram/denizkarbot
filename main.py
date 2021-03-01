import discord
import os
import requests
import json
import random
import asyncio
from requests.exceptions import RequestException
#Version command output
version = "Denizkar Bot's version is currently version 0.2.0"

#Changelogs
changelogstxt = "***Version 0.1.0:*** Added `unsad,` `coin,` `test,` `ram,` and `test` commands, and some things to help when you're sad. \n \n ***Version 0.1.1:*** Added `version,` `changelogs,` and `toadd` commands.\n \n ***Version 0.1.11:*** Fixed typos in the changelogs and made the format of the version easier to read.\n \n ***Version 0.1.12:*** Fixed a single typo in the `toadd` command and updated `toadd`. Also trying something with the changelogs \n \n ***Version 0.1.13:*** unnecessary brackets in changelogs removed.\n \n ***Version 0.2.0:*** \n\n  Optimized code and added comments to code to make it more readable, added `prefix` command (wip), removed `test` command, changed formatting of changlogs and updated to-add list, added `rolecreate` command, and **changed default prefix to !den**. \n \n ***Version 0.2.1:*** added the `makesad` command \n \n ***Version 0.2.2:*** ` h` and sleepy well"

#Stuff to add
toaddtxt = "`More fun will be added soon. In the far future, administration stuff may be added, but the programmer does not know enough python atm. You can suggest ideas to add by messaging @RamRam#5806, or even better, just chat in the general chat of the Church of Ram.`"
client = discord.Client()

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
coin = ["Heads", "Tails"]

colours = [discord.Color.dark_orange(),discord.Color.orange(),discord.Color.dark_gold(),discord.Color.gold(),discord.Color.dark_magenta(),discord.Color.magenta(),discord.Color.red(),discord.Color.dark_red(),discord.Color.blue(),discord.Color.dark_blue(),discord.Color.teal(),discord.Color.dark_teal(),discord.Color.green(),discord.Color.dark_green(),discord.Color.purple(),discord.Color.dark_purple()]

from discord.ext import commands
bot = commands.Bot(command_prefix='!den ')

		
@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
	h='h','H'
	msg = message.content
	gn='gn', 'Gn', 'gn!', 'Gn!'
	if message.author == bot.user:	
		return
	if any(word in msg for word in sad_words): #detect sad words
		await message.channel.send(random.choice(starter_encouragements)) #send encouragements
	if  msg in h: #detect h
		await message.channel.send('h') #send h
	await bot.process_commands(message)
	if  msg in gn: #detect gn
		await message.channel.send('Sleepy well, cutie! :3') #send h
	await bot.process_commands(message)


@bot.command(name='unsad', help= 'use this when you\'re sad =}', Category='Cheerful')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def unsad(ctx):
	
	def get_quote():
		response = requests.get("https://zenquotes.io/api/random")
		json_data = json.loads(response.text)
		quote = json_data[0]['q'] + " -" + json_data[0]['a']
		asyncio.sleep(1)
		return (quote)
		
	quote = get_quote()
	
	await ctx.send(quote)

@bot.command(name='ram', help='you\'ll find out what this does if you use it', Category='Fun')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def ram(ctx):
		await ctx.send('Ram is best girl, but we all know that I am second best =}')




@bot.command(name='coin', help='flip a coin', Category='Utility')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def coin(ctx):
	await ctx.send(random.choice(coin))

@bot.command(name='version', help='Version of the bot.', Category='Bot Info')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def version(ctx):
	await ctx.send(version)

@bot.command(name='changelogs', help= 'Recent changes to the bot. Probably not helpful because they\'re likely outdated or have typos', Category='Bot Info')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def changelogs(ctx):
	await ctx.send(changelogstxt)

@bot.command(name='toadd', help='Things that are likely be added to Denizkar Bot in the future. Probably changes frequently idk', Category='Bot Info')
@commands.cooldown(1, 1, commands.BucketType.guild)
async def toadd(ctx):
	await ctx.send(toaddtxt)

@bot.command(name='rolecreate', help='create a role with a hex color')
@commands.cooldown(1, 1, commands.BucketType.guild)
@commands.has_permissions(manage_roles=True)
async def rolecreate(ctx, name, color):
	print('command started')
	guild=ctx.guild
	colorhex=int(color,16)
	await guild.create_role(name=name, color=discord.Colour(colorhex))
	await ctx.send(f'Role `{name}` has been created""')
	
@bot.command(name="makesad", help="sends an ai-generated quote to probably make you sadn't")
@commands.cooldown(1, 1, commands.BucketType.guild)
async def makesad(ctx):

	# sends GET request to Inspirobot for image url response
	try:
		url = 'http://inspirobot.me/api?generate=true'
		params = {'generate' : 'true'}
		response = requests.get(url, params, timeout=10)
		image = response.text
		await ctx.send(image)
		
	except RequestException:
		
		await ctx.send('Inspirobot is broken, there is no reason to live.')
import keep_alive
keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))
