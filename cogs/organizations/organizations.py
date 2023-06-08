import discord
from discord.ext import commands
import cogs.create.create as create
from lib import sQl_bot, checks
from lists import Ogr_info, resources
import random 
from datetime import timedelta, datetime

def checks_org(id, interaction):
    if sQl_bot.check_table(id, "users", "organization")["organization"] != list(Ogr_info)[0]:
        interaction_yes = interaction.response.send_message("Ты состоишь в орагнизации", ephemeral = True)
        return True, interaction_yes
    else:
        interaction_no = interaction.response.send_message("Ты не состоишь в организации", ephemeral = True)
        return False, interaction_no



class Organiz(commands.Cog): # Основная панель
    def __init__(self, Bot: discord.Bot):
        self.Bot = Bot

    @discord.slash_command(name = "организация", description="профиль организации") 
    async def organiz(self, ctx):
        try:
            if sQl_bot.check_table(ctx.author.id,'users', 'organization')['organization'] == list(Ogr_info)[0]:
                embed = discord.Embed(
                    title=f"Вступить в организацию",
                    description="Описание (В разработке)",
                    color=discord.Colour.random(), 
                ) 

                await ctx.respond(embed = embed, view = Organiz_Сhoice(ctx.author.id))
            else:
                org = sQl_bot.check_table(ctx.author.id,'users', "organization, org_post, experience, tool")

                embed = discord.Embed(
                    title=f"Твоя организация {org['organization']}",
                    description=f"Описание (В разработке)\nДолжнось: {org['org_post']}\nСтаж: {org['experience']}",
                    color= 0x1faee9, # цвет твиттера
                ) 

                await ctx.respond(embed = embed, view = OrganizPanel(ctx.author.id, org))
        except (discord.errors.ApplicationCommandInvokeError, TypeError): 
            await ctx.respond("Ты еще не создал персонажа. Нажми на заветную кнопку и начни покорять этот мир!!!", view = create.createView(), ephemeral=True)


class Organiz_Сhoice(discord.ui.View): # Вызывает панель с выбором организации
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

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif c_org[0]:
            await c_org[1]

        else:
            organization = select.values[0] 
            await interaction.message.edit(
                f"Договор о вступлении в {select.values[0]}!", 
                embed = None, 
                view = Organiz_join_View(interaction.user.id, organization))
            
            await interaction.response.defer()

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
        
        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        elif datetime.now() < (time()["Time"] + timedelta(hours=4)):
            
            time_difference = datetime.now() - (time()["Time"] + timedelta(hours=4))
            hours = int(time_difference.total_seconds() / 3600)   # Переводим секунды в часы 
            minutes = int((time_difference.total_seconds() - (hours * 3600)) / 60)

            await interaction.response.send_message(content=f"Потом поработай, ок? через {hours} часов и {minutes} минут", ephemeral=True)
        else:
            Role = self.org['organization'] # Моя организация
            rang = self.org['org_post'] # Мой ранг в организации
            tool = self.org["tool"]
            tools_list = Ogr_info[Role]["Инструменты"]
            boost = tools_list.get(tool, {"Буст": 1})["Буст"]
            multiplier = 1 * boost

            my_salary = int(Ogr_info[Role]["Должность"][rang] * multiplier) # моя зп

            salary = random.randint(my_salary // 2, my_salary)

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

            
            await interaction.message.edit(
                "Ты заработал {0} {1}".format(salary, resources["gems"]), embed = None, 
                view = None)

    @discord.ui.button(label = 'Повышение', style=discord.ButtonStyle.primary) 
    async def organiz_work_up(self, button, interaction):       

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            ex = self.org['experience']
            Ogr = self.org['organization']
            Rang = self.org['org_post']
            Roles = Ogr_info[Ogr]["Должность"]

            x = list(Ogr_info[Ogr]["Должность"])
            user_index = x.index(Rang)
            NewRole = x[user_index + 1]

            if user_index + 1 > 3:
                await interaction.response.send_message(f"Ты уже достиг максимальной должности!!!", ephemeral=True)
            elif ex < (user_index + 1) * 5:
                await interaction.response.send_message(f"До повышения осталось поработать {(user_index + 1) * 5 - ex} раз(а)", ephemeral=True)
            else:
                sQl_bot.update_table(
                    interaction.user.id, 
                    "users",
                    f"""`org_post` = '{NewRole}',
                        `experience` = 0
                    """
                )
                await interaction.message.edit(f"Поздравляю с повышением. Твоя новая должность {NewRole}, средний оклад {Roles[index + 1][NewRole]}", embed = None, view = None)


    @discord.ui.button(label = 'Уволится', style=discord.ButtonStyle.red) 
    async def organiz_leave(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            await interaction.message.edit(f"Ты уверен что хочешь уволится?", 
                                           embed = None, 
                                           view = Organiz_leave_View(interaction.user.id))
            await interaction.response.defer()


    @discord.ui.button(label = 'Магазин', style=discord.ButtonStyle.green, row=2) 
    async def organiz_shop(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            await interaction.message.edit(f"Магазин\nТут будет описание что есть иструменты или бусты", embed = None, view = Organiz_shop_choise(interaction.user.id))
            await interaction.response.defer()
class Organiz_shop_choise(discord.ui.View): # Вызывает панель с магазином
    def __init__(self, id):
        super().__init__()
        self.id = id
        
    @discord.ui.button(label = 'Инструменты', style=discord.ButtonStyle.gray) 
    async def organiz_shop_choise_tools(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            user_org_post = sQl_bot.check_table(interaction.user.id, "users", "organization")['organization']
            org_tools = Ogr_info[user_org_post]["Инструменты"]
            tools_list = list(org_tools)
            embed = discord.Embed(
                    title=f"Магазин инструментов '{user_org_post}'",
                    color=discord.Colour.random(), 
                ) 
            
            for i_tools, i_specifications in org_tools.items():
                embed.add_field(name=f"{i_tools}", 
                                value=f"""
Стоймость: {i_specifications["Стоймость"]} {resources["gems"]}\n
Бонус к добыче: x{i_specifications['Буст']}\n
Прочность: {i_specifications['Прочность']}
                                """, 
                                inline=True)

            await interaction.message.edit(f"", embed = embed, view = Organiz_shop_tools(interaction.user.id, user_org_post, tools_list))
            await interaction.response.defer()


    @discord.ui.button(label = 'Бусты', style=discord.ButtonStyle.gray) 
    async def organiz_shop_choise_boosters(self, button, interaction):
        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            await interaction.message.edit(f"Бусты. Пон?", embed = None, view = None)
            await interaction.response.defer()

    @discord.ui.button(label = 'Назад', style=discord.ButtonStyle.gray) 
    async def organiz_shop_choise_back(self, button, interaction):
        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            org = sQl_bot.check_table(interaction.user.id,'users', "organization, org_post, experience, tool")

            embed = discord.Embed(
                title=f"Твоя организация {org['organization']}",
                description=f"Описание (В разработке)\nДолжнось: {org['org_post']}\nСтаж: {org['experience']}",
                color= 0x1faee9, # цвет твиттера
            ) 

            await interaction.message.edit(embed = embed, view = OrganizPanel(interaction.user.id, org))
            await interaction.response.defer()

class Organiz_shop_tools(discord.ui.View):
    def __init__(self, id, org, tools_list):
        super().__init__()
        self.id = id
        self.tools_list = tools_list
        self.org = org

    @discord.ui.button(label = '1', style=discord.ButtonStyle.gray) 
    async def organiz_shop_tools_1(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        user_gems = sQl_bot.check_table(interaction.user.id, "users", "gems")["gems"]
        tools_gems = Ogr_info[self.org]["Инструменты"][self.tools_list[0]]["Стоймость"]

        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        elif sQl_bot.check_table(interaction.user.id, "users", "tool")["tool"] != None:
            await interaction.response.send_message(f"У тебя уже есть инструмент", ephemeral = True)
        elif self.org != sQl_bot.check_table(interaction.user.id, "users", "organization")["organization"]:
            await interaction.response.send_message(f"Ты состоишь в другой организации", ephemeral = True)
        elif user_gems < tools_gems:
            gems_icon = resources["gems"]
            Difference = tools_gems - user_gems
            await interaction.response.send_message(f"Недостаточно {Difference} {gems_icon}", ephemeral = True)

        else:
            sQl_bot.update_table(interaction.user.id, "users", f"""
            `tool` = '{self.tools_list[0]}',
            `gems` = `gems` - {tools_gems}""")
            await interaction.message.edit(f"Покупка успешна", embed = None, view = None)
            await interaction.response.defer()

    @discord.ui.button(label = '2', style=discord.ButtonStyle.gray) 
    async def organiz_shop_tools_2(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        user_gems = sQl_bot.check_table(interaction.user.id, "users", "gems")["gems"]
        tools_gems = Ogr_info[self.org]["Инструменты"][self.tools_list[0]]["Стоймость"]
        
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        elif sQl_bot.check_table(interaction.user.id, "users", "tool")["tool"] != None:
            await interaction.response.send_message(f"У тебя уже есть инструмент", ephemeral = True)
        elif self.org != sQl_bot.check_table(interaction.user.id, "users", "organization")["organization"]:
            await interaction.response.send_message(f"Вы состоите в другой организации", ephemeral = True)
        elif user_gems < tools_gems:
            gems_icon = resources["gems"]
            Difference = tools_gems - user_gems
            await interaction.response.send_message(f"Недостаточно {Difference} {gems_icon}", ephemeral = True)
        else:
            sQl_bot.update_table(interaction.user.id, "users", f"""
            `tool` = '{self.tools_list[1]}',
            `gems` = `gems` - {tools_gems}""")

            await interaction.message.edit(f"Покупка успешна", embed = None, view = None)
            await interaction.response.defer()

    @discord.ui.button(label = 'Назад', style=discord.ButtonStyle.gray, row = 2) 
    async def organiz_shop_tools_back(self, button, interaction):
        await interaction.message.edit(f"Магазин\nТут будет описание что есть иструменты или бусты", embed = None, view = Organiz_shop_choise(interaction.user.id))
        await interaction.response.defer()
        

class Organiz_join_View(discord.ui.View): # Вызывает панель с подтверждением для вступления в организацию
    def __init__(self, id, organization):
        super().__init__()
        self.id = id
        self.organization = organization

    @discord.ui.button(emoji = '✅', style=discord.ButtonStyle.gray) 
    async def organiz_join_yes(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif c_org[0]:
            await c_org[1]

        else:
            
            org_post = list(Ogr_info[self.organization]["Должность"])[0]
            sQl_bot.update_table(
                interaction.user.id,
                "users",
                f"""`organization` = '{self.organization}', `org_post` = '{org_post}'"""
            )
            await interaction.message.edit(f"Поздравляем вы вступили в организацию", view = None)
            await interaction.response.defer()
            
    @discord.ui.button(emoji = '❌', style=discord.ButtonStyle.gray) 
    async def organiz_join_no(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif c_org[0]:
            await c_org[1]

        else:

            embed = discord.Embed(
                title=f"Вступить в организацию",
                description="Описание (В разработке)",
                color=discord.Colour.random(), 
            ) 
            
            await interaction.message.edit(content = None,embed = embed, view = Organiz_Сhoice(interaction.user.id))
            await interaction.response.defer()

class Organiz_leave_View(discord.ui.View): # Вызывает панель с подтверждением для ухода из организации
    def __init__(self, id):
        super().__init__()
        self.id = id
        
            
    @discord.ui.button(emoji = '❌', style=discord.ButtonStyle.green) 
    async def organiz_leave_no(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:

            org = sQl_bot.check_table(interaction.user.id,'users', "organization, org_post, experience, tool")
            embed = discord.Embed(
                title=f"Твоя организация {org['organization']}",
                description=f"Описание (В разработке)\nДолжнось: {org['org_post']}\nСтаж: {org['experience']}",
                color= 0x1faee9, # цвет твиттера
            ) 

            await interaction.message.edit(content = None, embed = embed, view = OrganizPanel(interaction.user.id, org))
            await interaction.response.defer()

    @discord.ui.button(emoji = '✅', style=discord.ButtonStyle.red) 
    async def organiz_leave_yes(self, button, interaction):

        c_author = checks.check_author(interaction.user.id, self.id)
        c_org = checks_org(interaction.user.id, interaction)
        if c_author[0]:
            await c_author[1]
        elif not c_org[0]:
            await c_org[1]

        else:
            
            sQl_bot.update_table(
                interaction.user.id,
                "users",
                f"""`organization` = '{list(Ogr_info)[0]}', 
                `org_post` = NULL,
                `experience` = 0,
                `tool` = NULL,
                `tool_strength` = NULL 
                """
            )
            await interaction.message.edit(f"Ты уволился!", view = None)

def setup(bot):
    bot.add_cog(Organiz(bot)) 