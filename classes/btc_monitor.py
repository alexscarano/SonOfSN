import json
from discord.ext import tasks, commands
from datetime import timedelta, timezone
from helpers.fetch_btc import fetch_price
import os
import discord

DATA_PATH = "data/channels.json"

# Herda de dicord.Client
# Representa a entidade do bot e suas ações
class BTCMonitor(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)
        self.last_price = None


    def get_alert_channel(self, guild_id):
        # Lê o canal salvo no JSON
        if not os.path.exists(DATA_PATH):
            return None

        with open(DATA_PATH, "r") as f:
            data = json.load(f)

        return data.get(str(guild_id))

    @tasks.loop(hours=12)
    async def price_notifier(self):
        # Tarefa que roda a cada X segundos/minutos
        await self.wait_until_ready()
        try: 
            for guild in self.guilds:
                channel_id = self.get_alert_channel(guild_id=guild.id)
                if not channel_id:
                    continue

                channel = self.get_channel(channel_id)
                if not channel:
                    continue

                price, priceInBrl, change = await fetch_price()
                utc_minus_3 = timezone(timedelta(hours=-3))

                embed = discord.Embed(
                        title = "Preço do Bitcoin",
                        description=f"Preço atual do Bitcoin: **${price:,.2f}**",
                        color = discord.Colour.gold(),
                        timestamp = discord.datetime.now(utc_minus_3)
                    )

                if self.last_price is None:
                    embed.add_field(name="Variação 24h\n", value=f"{change:.2f}%", inline=False)
                    embed.add_field(name="Preço em BRL\n", value=f"{priceInBrl:,.2f}R$", inline=False)
                
                    embed.set_footer(text=f"Atualizado automaticamente pelo Son of S.N")
                    embed.set_thumbnail(url="https://cryptologos.cc/logos/bitcoin-btc-logo.png")

                    await channel.send(embed=embed)
                else:
                    diff = price - self.last_price
                    embed.color = discord.Colour.green() if diff >= 0 else discord.Colour.dark_red()
                    direction = "subiu, ta magnata em (￣y▽￣)╭  hihihi" if diff >= 0 else "ヾ(•ω•`)o eiii caiu está na hora de comprar"
                    
                    embed.add_field(name="Diferença desde última\n ", value=f"${diff:,.2f}", inline=False)
                    embed.add_field(name="Variação 24h\n", value=f"{change:.2f}%", inline=False)
                    embed.add_field(name="Preço em BRL\n", value=f"{priceInBrl:,.2f}R$", inline=False)
                    embed.add_field(name="Status\n", value=f"{direction}", inline=False)
                    embed.set_footer(text=f"Atualizado automaticamente pelo Son of S.N")
                    embed.set_thumbnail(url="https://logos-world.net/wp-content/uploads/2020/08/Bitcoin-Logo.png")
                        
                    await channel.send(embed=embed)

            self.last_price = price
            
        except Exception as e:
            # debug 
            print(f"Ocorreu um erro ao buscar, {e}")

    async def setup_hook(self):
        await self.tree.sync()  # sincroniza todos os comandos com os servidores
        await self.load_cogs()
        self.price_notifier.start()

    async def load_cogs(self):
        for cog in os.listdir('classes/cogs'):
            if cog.endswith('.py'):
                await self.load_extension(f'classes.cogs.{cog[:-3]}')
