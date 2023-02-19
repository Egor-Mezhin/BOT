import discord
from discord.ext import commands
import cogs.create.create as create
from config import connection
from lib import sQl_bot
from lists import Ogr_post
from random import randrange

class Organiz(commands.Cog): 
    def __init__(self, Bot: discord.Bot):
        self.Bot = Bot

    @discord.slash_command(name = "организация", description="профиль организации") 
    async def organiz(self, ctx):

        if sQl_bot.check_users(ctx.author.id, 'id') == None:
            await ctx.response.send_message("Ты еще не создал персонажа. Нажми на заветную кнопку и начни покорять этот мир!!!", view = create.createView(), ephemeral=True)
        elif ''.join(sQl_bot.check_users(ctx.author.id, 'organization')['organization']) == ''.join(list(Ogr_post)[0]):
            embed = discord.Embed(
                title=f"Вступить в организацию",
                description="Описание (В разработке)",
                color=discord.Colour.random(), 
            ) 
            await ctx.respond(embed = embed, view = OrganizView(ctx.author.id))
        else:
            org = sQl_bot.check_users(ctx.author.id, "organization, org_post")
            embed = discord.Embed(
                title=f"Твоя организация {org['organization']}",
                description=f"Описание (В разработке)\nДолжнось: {org['org_post']}",
                color= 0x1faee9, # цвет твиттера
            ) 

            await ctx.respond(embed = embed, view = OrganizPanel(ctx.author.id, org))


class OrganizView(discord.ui.View): # Вызывает панель с выбором организации
    def __init__(self, id):
        super().__init__()
        self.id = id

    @discord.ui.select( 
        placeholder = "Устройтесь на работу своей мечты!!!",
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="Шахта",
                description="Добывай железо"
            ),
            discord.SelectOption(
                label="Лесопилка",
                description="Добывай древесину"
            ),
            discord.SelectOption(
                label="Органический сад",
                description="Добывай органику"
            ),
            discord.SelectOption(
                label="Завод",
                description="Делай детали"
            ),
            discord.SelectOption(
                label="Электростанция",
                description="Добывай Энергию"
            ),
            discord.SelectOption(
                label="Лаборатрия 903",
                description="Иследуй магию"
            )
        ]
    )
    async def organiz_join(self, select, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            organization = select.values[0] 
            await interaction.response.send_message(f"Договор о вступлении в {select.values[0]}!", view = Organiz_join_View(interaction.user.id, organization))


class Organiz_join_View(discord.ui.View): # Вызывает панель с подтверждением
    def __init__(self, id, organization):
        super().__init__()
        self.id = id
        self.organization = organization

    @discord.ui.button(emoji = '✅', style=discord.ButtonStyle.gray) 
    async def organiz_join_yes(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            
            org_post = ''.join(list(Ogr_post[self.organization][0]))
            with connection.cursor() as cursor:
                ogr =(
                        f"""
                        UPDATE `discord`.`users` 
                        SET `organization` = '{self.organization}',
                        `org_post` = '{org_post}'
                        WHERE `user_id` = '{interaction.user.id}';
                        """)
                ogr = cursor.execute(ogr)
                ogr = cursor.fetchone() 
                connection.commit()

            await interaction.response.send_message(f"Поздравляем вы вступили в организацию", view = None)
            
    @discord.ui.button(emoji = '❌', style=discord.ButtonStyle.gray) 
    async def organiz_join_no(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:

            embed = discord.Embed(
                title=f"Вступить в организацию",
                description="Описание (В разработке)",
                color=discord.Colour.random(), 
            ) 
            
            await interaction.response.send_message(embed = embed, view = OrganizView(interaction.user.id))

class OrganizPanel(discord.ui.View): # Вызывает панель с выбором организации
    def __init__(self, id, org):
        super().__init__()
        self.id = id
        self.org = org
        
    @discord.ui.button(label = 'Работать', style=discord.ButtonStyle.green) 
    async def organiz_work(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            payment = Ogr_post
            await interaction.response.send_message(f"Ты заработал{randrange(1, 100)}", view = None)

    @discord.ui.button(label = 'Повышение', style=discord.ButtonStyle.primary) 
    async def organiz_work_up(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            await interaction.response.send_message(f"В разработке...", view = None)


def setup(bot):
    bot.add_cog(Organiz(bot)) 