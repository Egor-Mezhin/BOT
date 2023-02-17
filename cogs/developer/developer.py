import discord
from discord.ext import commands
from config import connection
import os


class Developer(commands.Cog): 
    pass
    # @discord.slash_command(name = "dev", description="панель разработчика") 
    # async def createF(self, ctx):
    #     if ctx.author.id != 567107484850847744:
    #         await ctx.send('Размечтался', ephemeral=True)
    #     else:
    #         embed = discord.Embed(
    #             title="Панель разработки",
    #             color=discord.Colour.blue(),
    #         )
    #         await ctx.delete()
    #         await ctx.send(embed = embed, view = DeveloperView())

class DeveloperView(discord.ui.View): 
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Перезапуск бота", custom_id="Developer-1", style=discord.ButtonStyle.red) 
    async def restart_button(self, button, interaction):
        if interaction.user.id != 567107484850847744:
            await interaction.response.send_message('Размечтался', ephemeral=True)
        else:
            await interaction.response.defer()
            os.system("server.bat")
            # clear = lambda: os.system('cls')
            # clear()
            print("Бот Перезапущен Успешно")


    @discord.ui.button(label="Очистка консоли", custom_id="Developer-2", style=discord.ButtonStyle.red) 
    async def console_clear_button(self, button, interaction):
        if interaction.user.id != 567107484850847744:
            await interaction.response.send_message('Размечтался', ephemeral=True)
        else:
            await interaction.response.defer()
            clear = lambda: os.system('cls')
            clear()
    
    @discord.ui.button(label="вызвать панель", custom_id="Developer-3", style=discord.ButtonStyle.primary) 
    async def devpanel_button(self, button, interaction):
        if interaction.user.id != 567107484850847744:
            await interaction.response.send_message('Размечтался', ephemeral=True)
        else:
            embed = discord.Embed(
                title="Панель разработки",
                color=discord.Colour.blue(),
            )
            await interaction.response.send_message(embed = embed, view = DeveloperView())
            await interaction.response.defer()

    # @discord.ui.button(label="SQL", custom_id="Developer-4", style=discord.ButtonStyle.primary) 
    # async def SQL_button(self, button, interaction):
    #     if interaction.user.id != 567107484850847744:
    #         await interaction.response.send_message('Размечтался', ephemeral=True)
    #     else:
    #         with connection.cursor() as cursor:
                
    #             SQL = cursor.execute(SQL)
    #             SQL = cursor.fetchone()
    #             connection.commit()
    #             print(SQL)

 

def setup(bot):
    bot.add_cog(Developer(bot)) 