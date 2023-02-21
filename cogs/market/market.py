import discord
from discord.ext import commands
from config import connection
from lists import resources
count = 1 # Переменная колличества товара


resourceName = { # Список эмодзи присвоеных именам опциям в селект меню
    'Железо': resources['iron'],
    'Древесина': resources['organic'],
    'Органика': resources['wood'],
    'Детали': resources['details'],
    'Батарейки': resources['batteries'],
    'Осколки': resources['shards'],
} 

class Market(commands.Cog): # Вызывает Рынок
    def __init__(self, Bot: discord.Bot):
        self.Bot = Bot

    @discord.slash_command(name = "рынок", description="открывает рынок столицы") 
    async def createF(self, ctx):
        embed = discord.Embed(
            title="Рынок",
            description="В разработке...",
            color=discord.Colour.random(),
        )
        await ctx.respond(embed = embed, view = MarketView(ctx.author.id))

class MarketView(discord.ui.View): # Селект меню для рынка
    def __init__(self, id):
        super().__init__()
        self.id = id

    @discord.ui.select( 
            placeholder = "🔺 | Купить", 
            min_values = 1, 
            max_values = 1, 
            options = [ 
                discord.SelectOption(
                    label="Железо",
                    description=f"Цена: X за штуку",
                    emoji= resources['iron']
                ),
                discord.SelectOption(
                    label="Древесина",
                    description=f"Цена: X за штуку",
                    emoji= resources['organic']
                ),
                discord.SelectOption(
                    label="Органика",
                    description=f"Цена: X за штуку",
                    emoji= resources['wood']
                ),
                discord.SelectOption(
                    label="Детали",
                    description=f"Цена: X за штуку",
                    emoji= resources['details']
                ),
                discord.SelectOption(
                    label="Батарейки",
                    description=f"Цена: X за штуку",
                    emoji= resources['batteries']
                ),
                discord.SelectOption(
                    label="Осколки",
                    description=f"Цена: X за штуку",
                    emoji= resources['shards']
                )
            ]
    )
    async def select_buy(self, select, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator # Переменные колличества товара, название выбранного товара + его эмодзи и оператор покупки или продажи
            operator = True
            selectName = resourceName[select.values[0]]
            embed = discord.Embed(
                title=f"Сколько **{selectName}** вы хотите купить?",
                description=f"{count}",
                color=discord.Colour.blue(),
            )
            await interaction.response.edit_message(embed = embed, view = СalculatorView(interaction.user.id))


    @discord.ui.select( 
            placeholder = "🔻 | Продать", 
            min_values = 1, 
            max_values = 1, 
            options = [ 
                discord.SelectOption(
                    label="Железо",
                    description=f"Цена: X за штуку",
                    emoji= resources['iron']
                ),
                discord.SelectOption(
                    label="Древесина",
                    description=f"Цена: X за штуку",
                    emoji= resources['organic']
                ),
                discord.SelectOption(
                    label="Органика",
                    description=f"Цена: X за штуку",
                    emoji= resources['wood']
                ),
                discord.SelectOption(
                    label="Детали",
                    description=f"Цена: X за штуку",
                    emoji= resources['details']
                ),
                discord.SelectOption(
                    label="Батарейки",
                    description=f"Цена: X за штуку",
                    emoji= resources['batteries']
                ),
                discord.SelectOption(
                    label="Осколки",
                    description=f"Цена: X за штуку",
                    emoji= resources['shards']
                )
            ]
    )
    async def select_sell(self, select, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator # Переменные колличества товара, название выбранного товара и оператор покупки или продажи
            operator = False
            selectName = resourceName[select.values[0]]
            embed = discord.Embed(
                title=f"Сколько **{selectName}** вы хотите продать?",
                description=f"{count}",
                color=discord.Colour.blue(),
            )
            await interaction.response.edit_message(embed = embed, view = СalculatorView(interaction.user.id))
        

class СalculatorView(discord.ui.View): # Кнопки калькулятора для покупки или продажи
    def __init__(self, id):
        super().__init__()
        self.id = id

    @discord.ui.button(label="+1", style=discord.ButtonStyle.primary, row=1) 
    async def buysell_button_p1(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator
            count += 1
            if operator:
                embed = discord.Embed(
                    title=f"Сколько **{selectName}** вы хотите купить?",
                    description=f"{count}",
                    color=discord.Colour.blue(),
                )
            await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="+10", style=discord.ButtonStyle.primary, row=1) 
    async def buysell_button_p10(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator
            count += 10
            if operator:        
                embed = discord.Embed(
                    title=f"Сколько **{selectName}** вы хотите купить?",
                    description=f"{count}",
                    color=discord.Colour.blue(),
                )
            await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="+100", style=discord.ButtonStyle.primary, row=1) 
    async def buysell_button_p100(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator
            count += 100
            if operator:
                embed = discord.Embed(
                    title=f"Сколько **{selectName}** вы хотите купить?",
                    description=f"{count}",
                    color=discord.Colour.blue(),
                )
            await interaction.response.edit_message(embed = embed)
    
    @discord.ui.button(style=discord.ButtonStyle.green, emoji = "🪙", row=1) # emoji монетки
    async def buysell_button(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator, operator

            if operator:
                embed = discord.Embed(
                    title=f"Ты купил {count} {selectName} но в балансе их пока нет. потом дам)",
                    description=f"Ты купил {count} {selectName} но в балансе их пока нет. потом дам)",
                    color=discord.Colour.blue(),
                )
                await interaction.response.edit_message(embed = embed, view = None)

            else:
                embed = discord.Embed(
                    title=f"Ты продал {count} {selectName} но в балансе их пока нет. потом дам)",
                    description=f"Ты продал {count} {selectName} но в балансе их пока нет. потом дам)",
                    color=discord.Colour.blue(),
                )
                await interaction.response.edit_message(embed = embed, view = None)            

    @discord.ui.button(label="-1", style=discord.ButtonStyle.primary, row=2) 
    async def buysell_button_m1(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator
            if count - 1 < 1:
                await interaction.response.send_message("Вы не можете выбрать товар меньше еденицы", ephemeral=True)
            else:
                count -= 1
                if operator:
                    embed = discord.Embed(
                        title=f"Сколько **{selectName}** вы хотите купить?",
                        description=f"{count}",
                        color=discord.Colour.blue(),
                    )
                await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="-10", style=discord.ButtonStyle.primary, row=2) 
    async def buysell_button_m10(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator
            if count - 10 < 1:
                await interaction.response.send_message("Вы не можете выбрать товар меньше еденицы", ephemeral=True)
            else:
                count -= 10
                if operator:
                    embed = discord.Embed(
                        title=f"Сколько **{selectName}** вы хотите купить?",
                        description=f"{count}",
                        color=discord.Colour.blue(),
                    )
                await interaction.response.edit_message(embed = embed)

    @discord.ui.button(label="-100", style=discord.ButtonStyle.primary, row=2) 
    async def buysell_button_m100(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
        else:
            global count, selectName, operator
            if count - 100 < 1:
                await interaction.response.send_message("Вы не можете выбрать товар меньше еденицы", ephemeral=True)
            else:
                count -= 100
                if operator:
                    embed = discord.Embed(
                        title=f"Сколько **{selectName}** вы хотите купить?",
                        description=f"{count}",
                        color=discord.Colour.blue(),
                    )
                await interaction.response.edit_message(embed = embed)
        
def setup(bot):
    bot.add_cog(Market(bot)) 
