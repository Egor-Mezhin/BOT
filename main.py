import discord
import os 
from dotenv import load_dotenv
import cogs.create.create as create
import cogs.developer.developer as developer
from config import connection 
from lib import sQl_bot

load_dotenv() 
bot = discord.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user} готов к работе!!!")
    bot.add_view(create.createView())
    bot.add_view(developer.DeveloperView())

cogs_list = (
    'panel.panel',
    'developer.developer',
    'create.create',
    'market.market',
    'organizations.organizations'
)

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.slash_command(name = "test", description="test") 
async def organiz(ctx):
    x = ''.join(sQl_bot.check_table(ctx.author.id,'users', 'organization')['organization'])
    y = sQl_bot.check_table(ctx.author.id,'users', 'organization')['organization']
    await ctx.respond(f"{x}\n{y}", view = Test_Buttons(ctx.author.id))

class Test_Buttons(discord.ui.View): # Вызывает панель с подтверждением для вступления в организацию
    def __init__(self, id):
        super().__init__()
        self.id = id


    @discord.ui.button(emoji = '✅', style=discord.ButtonStyle.gray) 
    async def Test_Button(self, button, interaction):
            num = sQl_bot.check_table(self.id, "users", "number")["number"]
            print(num)
            
            if num == 1:
                sQl_bot.update_table(self.id, "users", "`number` = 2")
                await interaction.response.send_message("1 ----> 2")
            else:
                await interaction.response.send_message("Error")
        
        

bot.run(os.getenv('TOKEN')) 

        