import discord
from discord.ext import commands
import cogs.panel.ViewPanel as panel
import cogs.create.create as create
from config import connection


class Panel(commands.Cog): 
    def __init__(self, Bot: discord.Bot):
        self.Bot = Bot

    @discord.slash_command(name = "профиль", description="показывает твой профиль") 
    async def profile(self, ctx):
        try:
            with connection.cursor() as cursor:
                select =(
                        f"""SELECT organization as 'Организация'
                        FROM users
                        WHERE user_id = {ctx.author.id}""")
                select = cursor.execute(select)
                select = cursor.fetchone() 
            embed = discord.Embed(
                title=f"Профиль {ctx.author.name}",
                description=f"Организация: {select['Организация']}",
                color=discord.Colour.random(), 
            )

            embed.set_thumbnail(url= ctx.author.avatar)

            await ctx.respond(embed = embed, view=panel.PanelView(ctx.author.id))

        except (discord.errors.ApplicationCommandInvokeError, TypeError): 
            await ctx.respond("Ты еще не создал персонажа. Нажми на заветную кнопку и начни покорять этот мир!!!", view = create.createView(), ephemeral=True)



def setup(bot):
    bot.add_cog(Panel(bot)) 