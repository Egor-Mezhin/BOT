import discord
from discord.ext import commands
import cogs.create.create as create
from lists import resources, Ogr_info
from lib import sQl_bot, checks



class Panel(commands.Cog): 
    def __init__(self, Bot: discord.Bot):
        self.Bot = Bot

    @discord.slash_command(name = "профиль", description="показывает твой профиль") 
    async def profile(self, ctx):
        try:
            user_info = sQl_bot.check_table(ctx.author.id, "users", 
                                            """organization as Организация, 
                                            org_post as Должность, 
                                            experience as Стаж, 
                                            tool as Инструмент, 
                                            tool_strength as Прочность""")
            
            if user_info['Организация'] == list(Ogr_info)[0]:
                user_info_embed = {'Организация': user_info['Организация']}
            else:
                user_info_embed = user_info

            Ogr_list = list(Ogr_info[user_info['Организация']]["Должность"])
            user_index = Ogr_list.index(user_info['Должность'])
            embed = discord.Embed(
                title=f"Профиль {ctx.author.name}",
                color=discord.Colour.random(), 
            )

            user_org_info = f"""
{user_info_embed["Должность"]}
            """

            embed.add_field(name= user_info['Организация'], value=user_org_info, inline=True)
            embed.set_thumbnail(url= ctx.author.avatar)

            await ctx.respond(embed = embed, view=PanelView(ctx.author.id))

        except (discord.errors.ApplicationCommandInvokeError, TypeError): 
            await ctx.respond("Ты еще не создал персонажа. Нажми на заветную кнопку и начни покорять этот мир!!!", view = create.createView(), ephemeral=True)

class PanelView(discord.ui.View): # Вызывает панель с балансом игрока
    def __init__(self, id):
        super().__init__()
        self.id = id
                    
    @discord.ui.button(label="Баланс", style=discord.ButtonStyle.primary) 
    async def button_callback(self, button, interaction):
        c_author = checks.check_author(interaction.user.id, self.id)
        if c_author[0]:
            await c_author[1]
        else:
            balance = sQl_bot.check_table(
                interaction.user.id,
                'users',
                f"""
                gems as '{resources.get('gems')}',
                iron as '{resources.get('iron')}',
                wood as '{resources.get('organic')}',
                organic as '{resources.get('wood')}',
                parts as '{resources.get('details')}',
                batteries as '{resources.get('batteries')}',
                shards as '{resources.get('shards')}'
                """
                )

            embed = discord.Embed(
                title=f"Баланс {interaction.user.name}",
                description="Описание (В разработке)",
                color=discord.Colour.random(),
            )


            user_balance = "" # Записывает в колонку эмодзи ресурса и его колличество
            for i in balance.keys():
                user_balance += f"{i} {balance[i]} \n"
            embed.add_field(name="Баланс", value=user_balance, inline=True)

            embed.set_thumbnail(url= interaction.user.avatar)
            await interaction.response.edit_message(embed = embed, view = None)

def setup(bot):
    bot.add_cog(Panel(bot)) 