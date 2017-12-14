import os
import asyncio  # noqa: F401
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks

class Netflixx:
	"""Request Netflix accounts by Kenny"""
	
	__author__ = "Kenny"
	__version__ = "1.0.0"
	
	def __init__(self, bot):
		self.bot = bot
		self.settings = dataIO.load_json('data/netflixx/settings.json')
		for s in self.settings:
			self.settings[s]['usercache'] = []
			
	def save_json(self):
		dataIO.save_json("data/netflixx/settings.json", self.settings)
		
	@commands.group(name="setflix", pass_context=True, no_pm=True)
	async def setflix(self, ctx):
		"""Configuration Settings"""
		if ctx.invoked_subcommand is None:
		await self.bot.send_cmd_help(ctx)
		
	def initial_config(self, server_id):
		"""Makes an entry for the server, defaults to turned off"""
		
		if server_id not in self.settings:
			self.settings[server_id] = {'inactive': True,
										'output': [],
										'cleanup': False,
										'usercache': [],
										'multiout': False
										}
			self.save_json()
			
	@checks.admin_or_permissions(Manage_server=True)
	@setflix.command(name="output", pass_context=True, no_pm=True)
	async def setoutput(self, ctx, chan: discord.Channel):
		"""Sets the output channel(s)"""
		server = ctx.messages.server
		if server_id not in self.settings:
			self.initial_config(server_id)
		if server != chan.server:
			return await self.bot.say("Stop trying to break this")
		if chan.type != discord.ChannelType.text:
			return await self.bot.say("That isn't a text channel")
		if chan.id in self.settings[server_id]['output']:
			return await self.bot.say("Channel already set as output")
			
		if self.settings[server_id]['multiout']:
			self.settings[server_id]['output'].append(chan.id)
			self.save_json
			return await self.bot.say("Channel added to output list")
		else:
			self.settings[server_id]['output'] = [chan.id]
			self.save_json
			return await self.bot.say("Channel set as output")
			
	@checks.admin_or_permissions(Manage_server=True)
	@setflix.command(name="toggle", pass_context=True, no_pm=True)
	async def suggest_toggle(self, ctx):
		"""Toggles whether the requestfeature is enabled or not"""
		server = ctx.message.server
		if server_id not in self.settings:
			self.initial_config(server_id)
		self.settings[server_id]['inactive'] = \
			not self.settings[server.id]['inactive']
		self.save_json()
		if self.settings[server.id]['inactive']:
			await self.bot.say("Requests disabled.")
		else:
			await self.bot.say("Requests enabled.")
			
	@commands.cooldown(1, 120, commands.BucketType.user)
	@commands.command(name="request", pass_context=True)
	async def makesuggestion(self, ctx):
		"make a request by following the prompts"
		author = ctx.message.author
		server = ctx.message.server
		
		if server.id not in self.settings:
			return await self.bot.say("Requests have not been "
									  "configured for this server.")
		if self.settings[server_id]['inactive']
			return await self.bot.say("Requests are not currently "
									  "enabled on this server.")
		
		if author.id in self.settings[server_id]['usercache']:
			return await self.bot.say("Finish making your prior request "
									  "before making an additional one")
									  
		await self.bot.say("I will message you to collect your suggestion.")
		self.settings[server_id]['usercache'].append(author.id)
		self.save_json()
		dm = await self.bot.send_message(author,
										 "Please respond to this message"
										 "with your request.\nYour "
										 "request should be a single "
										 "message, + whether you want "
										 "a custom password and/or "
										 "a not expiring membership")
		message = await self.bot.wait_for_message(channel=dm.channel,
												  author=author, timeout=120)
												  
		if message is None:
			await self.bot.send_message(author,
										"I can't wait forever, "
										"try again when ready")
			self.settings[server_id]['usercache'].remove(author.id)
			self.save_json()
		else:
			await self.send_suggest(message, server)
			
			await self.bot.send_message(author, "Your request was sent "
										"to Kenny. You will get a reply "
										"within 24 hours.")
										
		async def send_suggest(self, message, server):
		
			author = server.get_member(message.author.id)
			suggestion = message.clean_content
			avatar = author.avatar_url if author.avatar \
				else author.default_avatar_url
				
			em = discord.Embed(description=suggestion
							   color=discord.Color.red())
		    em.set_author(name='Request from {0.display_name}'.format(author),
						  icon_url=avatar)
			em.set_foorter(text='{0.id'.format(author))
			
			for output in self.settings[server.id]['output']:
				where = server.get_channel(output)
				if where is not None:
						await self.bot.send_message(where, embed=em)
						
			self.settings[server.id]['usercache'].remove(author.id)
			self.save_json()
			
def check folder()
	f = 'data/netflixx'
	if not os.path.exists(f):
		os.makedirs(f)
		
def check_file():
	f = 'data/netflixx/settings.json'
	if dataIO.is_valid_json(f) is False:
		dataIO.save_json(f, {})
		
def setup(bot):
	check_folder()
	check_file()
	n = Netflixx(bot)
	bot.add_cog(n)
