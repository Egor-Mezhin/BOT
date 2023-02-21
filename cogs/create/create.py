import io
import discord
from discord.ext import commands
import pymysql
from config import connection
from PIL import Image   

class Create(commands.Cog): 
    pass
#     @discord.slash_command(name = "создание", description="показывает свой профиль") 
#     async def createF(self, ctx):
#         embed = discord.Embed(
#             title="Открой новый мир",
#             description="""
# Привет путник...\n
# Ищещь себя в этом забытом богами мире?\n
# Кто ты?...\n
# Герой? Вор? Драконоборец? Бизнесмен?\n
# Выбери свой путь, и пусть земля содрагаеться при виде нового игрока!!!
#             """,
#             color=discord.Colour.blue(),
#         )

#         File = [
#             discord.File("./cogs/create/img/create_img.jpg"),
#             discord.File("./cogs/create/img/create_th.png"),
#         ]

#         embed.set_thumbnail(url = 'attachment://create_th.png')
#         embed.set_image(url = "attachment://create_img.jpg")

#         embed.set_footer(text="| Обьедененое сообщество SK", icon_url = ctx.guild.icon.url)

#         await ctx.delete()
#         await ctx.send(files = File, embed = embed, view=createView())
        


class createView(discord.ui.View): # Создает персонажа
    def __init__(self):
        super().__init__(timeout=None)
            
    @discord.ui.button(label="Создать персонажа", custom_id="create-1", style=discord.ButtonStyle.primary) 
    async def create_button(self, button, interaction):
        try:

            with connection.cursor() as cursor:
            
                cursor.execute("""INSERT INTO users (user_id, user_name) 
                                VALUES (%s, %s);""", (interaction.user.id, interaction.user.name))   
                connection.commit()          
                
            await interaction.response.send_message('Персонаж создан', ephemeral=True)

        except (discord.errors.InteractionResponded, pymysql.err.Error):
            await interaction.response.send_message('Вы уже создавали персонажа ранее', ephemeral=True)
            


def setup(bot):
    bot.add_cog(Create(bot)) 