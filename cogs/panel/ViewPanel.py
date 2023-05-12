import discord
from lists import resources
from lib import sQl_bot


class PanelView(discord.ui.View): # Вызывает панель с балансом игрока
    def __init__(self, id):
        super().__init__()
        self.id = id
                    
    @discord.ui.button(label="Баланс", style=discord.ButtonStyle.primary) 
    async def button_callback(self, button, interaction):
        if interaction.user.id != self.id:
            await interaction.response.send_message(content="Ты не автор сообщения", ephemeral=True)
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