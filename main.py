import discord
import os 
from dotenv import load_dotenv
import cogs.create.create as create
import cogs.developer.developer as developer


load_dotenv() 
bot = discord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user} готов к работе!!!")
    bot.add_view(create.createView())
    bot.add_view(developer.DeveloperView())

cogs_list = [
    'panel.panel',
    'developer.developer',
    'create.create',
    'market.market',
    'organizations.organizations'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(os.getenv('TOKEN')) 

        