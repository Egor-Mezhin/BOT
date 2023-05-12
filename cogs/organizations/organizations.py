import discord
from discord.ext import commands
import cogs.create.create as create
from lib import sQl_bot, check_index
from lists import Ogr_info, resources
import random 
from datetime import timedelta, datetime

class Organiz(commands.Cog): 
    def __init__(self, Bot: discord.Bot):
        self.Bot = Bot

    @discord.slash_command(name = "организация", description="профиль организации") 
    async def organiz(self, ctx):

        if sQl_bot.check_table(ctx.author.id, 'users', 'id') == None:
            await ctx.response.send_message("Ты еще не создал персонажа. Нажми на заветную кнопку и начни покорять этот мир!!!", view = create.createView(), ephemeral=True)
        elif ''.join(sQl_bot.check_table(ctx.author.id,'users', 'organization')['organization']) == ''.join(list(Ogr_info)[0]):
            embed = discord.Embed(
                title=f"Вступить в организацию",
                description="Описание (В разработке)",
                color=discord.Colour.random(), 
            ) 
            await ctx.respond(embed = embed, view = OrganizView(ctx.author.id))
        else:
            org = sQl_bot.check_table(ctx.author.id,'users', "organization, org_post, experience")
            embed = discord.Embed(
                title=f"Твоя организация {org['organization']}",
                description=f"Описание (В разработке)\nДолжнось: {org['org_post']}\nСтаж: {org['experience']}",
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

class OrganizPanel(discord.ui.View): # Вызывает панель с организацией
    def __init__(self, id, org):
        super().__init__()
        self.id = id
        self.org = org
        
    @discord.ui.button(label = 'Работать', style=discord.ButtonStyle.green) 
    async def organiz_work(self, button, interaction):
        def time():
            time = sQl_bot.check_table(
                interaction.user.id,
                'user_cd', 
                'ogr_work as Time'
            )
            return time
    
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        elif datetime.now() < (time()["Time"] + timedelta(hours=4)):
            
            time_difference = datetime.now() - (time()["Time"] + timedelta(hours=4))
            hours = int(time_difference.total_seconds() / 3600)   # Переводим секунды в часы 
            minutes = int((time_difference.total_seconds() - (hours * 3600)) / 60)

            await interaction.response.send_message(content=f"Потом поработай, ок? через {hours} часов и {minutes} минут", ephemeral=True)
        else:


            Role = self.org['organization'] # Моя организация
            rang = self.org['org_post'] # Мой ранг в организации
            rangs = Ogr_info[Role] #Список рангов моей организации

            index = check_index(rangs, rang) # Поиск индекса моего ранга

            salary = random.randint(int(rangs[index][rang]) // 2, int(rangs[index][rang]))

            sQl_bot.update_table(
                interaction.user.id, 
                "users",
                f"""`gems` = `gems` + {salary},
                    `experience` = `experience` + 1
                """
                )
            sQl_bot.update_table(
                interaction.user.id, 
                "user_cd",
                "`ogr_work` = NOW()"
            )

            
            await interaction.response.send_message(
                "Ты заработал {0} {1}".format(salary, resources["gems"]), 
                view = None)

    @discord.ui.button(label = 'Повышение', style=discord.ButtonStyle.primary) 
    async def organiz_work_up(self, button, interaction):

        ex = self.org['experience']
        Role = self.org['organization'] 
        Rang = self.org['org_post']
        Roles = Ogr_info[Role]
        index = 0 
            
        for i in Roles:
            if list(i) == [Rang]:
                break
            index += 1
        NewRole = ''.join(Roles[index + 1])

        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        elif index + 1 > 3:
            await interaction.response.send_message(f"Ты уже достиг максимальной должности!!!", ephemeral=True)
        elif ex < (index + 1) * 5:
            await interaction.response.send_message(f"До повышения осталось поработать {(index + 1) * 5 - ex} раз(а)", ephemeral=True)
        else:
            sQl_bot.update_table(
                interaction.user.id, 
                "users",
                f"""`org_post` = '{NewRole}',
                    `experience` = 0
                """
            )
            await interaction.response.send_message(f"Поздравляю с повышением. Твоя новая должность {NewRole}, средний оклад {Roles[index + 1][NewRole]}", view = None)


    @discord.ui.button(label = 'Уволится', style=discord.ButtonStyle.red) 
    async def organiz_leave(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            await interaction.response.send_message(f"Ты уверен что хочешь уволится?", view = Organiz_leave_View(interaction.user.id))


    @discord.ui.button(label = 'Магазин', style=discord.ButtonStyle.green, row=2) 
    async def organiz_shop(self, button, interaction):
        pass

class Organiz_join_View(discord.ui.View): # Вызывает панель с подтверждением для вступления в организацию
    def __init__(self, id, organization):
        super().__init__()
        self.id = id
        self.organization = organization

    @discord.ui.button(emoji = '✅', style=discord.ButtonStyle.gray) 
    async def organiz_join_yes(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            
            org_post = ''.join(list(Ogr_info[self.organization][0]))
            sQl_bot.update_table(
                interaction.user.id,
                "users",
                f"""`organization` = '{self.organization}', `org_post` = '{org_post}'"""
            )
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

class Organiz_leave_View(discord.ui.View): # Вызывает панель с подтверждением для вступления в организацию
    def __init__(self, id):
        super().__init__()
        self.id = id
        
            
    @discord.ui.button(emoji = '❌', style=discord.ButtonStyle.green) 
    async def organiz_leave_no(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:

            org = sQl_bot.check_table(interaction.user.id,'users', "organization, org_post, experience")
            embed = discord.Embed(
                title=f"Твоя организация {org['organization']}",
                description=f"Описание (В разработке)\nДолжнось: {org['org_post']}\nСтаж: {org['experience']}",
                color= 0x1faee9, # цвет твиттера
            ) 
            
            await interaction.response.send_message(embed = embed, view = OrganizPanel(interaction.user.id, org))

    @discord.ui.button(emoji = '✅', style=discord.ButtonStyle.red) 
    async def organiz_leave_yes(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            
            sQl_bot.update_table(
                interaction.user.id,
                "users",
                f"""`organization` = '{''.join(list(Ogr_info)[0])}', 
                `org_post` = NULL,
                `experience` = 0
                """
            )
            await interaction.response.send_message(f"Ты уволился!", view = None)

def setup(bot):
    bot.add_cog(Organiz(bot)) 