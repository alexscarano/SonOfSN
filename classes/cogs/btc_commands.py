from datetime import datetime
from io import BytesIO
import discord
from discord.ext import commands
from matplotlib import pyplot as plt
import matplotlib.dates as mdates 
from helpers.fetch_btc import fetch_price
import requests

class BotCommands(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
        
        @commands.command(name='converter', description='Converte um valor de BTC para USD/BRL', help='Converte um valor de BTC para USD/BRL')
        async def convert(self, ctx: commands.Context, amount: float):
            priceInUSD, priceInBrl, _ = await fetch_price()

            totalInBrl = float(amount * priceInBrl)
            totalInUSD = float(amount * priceInUSD)

            embed = discord.Embed(
                title="💱 Conversão BTC",
                color= discord.Color.gold(),
                description=f"Conversão de **{amount:,.6f} BTC**"
            )   

            embed.add_field(name="Em USD", value=f"**${totalInUSD:,.2f}**", inline=True)
            embed.add_field(name="Em BRL", value=f"**R${totalInBrl:,.2f}**", inline=True)

            embed.set_thumbnail(url="https://logos-world.net/wp-content/uploads/2020/08/Bitcoin-Logo.png")
            embed.set_footer(text="Cotação em tempo real via CoinGecko")

            await ctx.reply(embed=embed, ephemeral=True)

        @commands.command(name='grafico', description='Mostra gráfico do Bitcoin (1d, 7d, 1m, 6m)', help='Mostra gráfico do Bitcoin (24h, 7d, 1m, 6m)')
        async def btc_graph(self, ctx: commands.Context, period: str = "24h"):
            period_list = ["1d", "7d", "1m", "6m"]

            if period not in period_list:
                 await ctx.reply("O.O periódo inválido, por favor use **1d**, **7d**, **1m**, **6**")
                 return

            if period == "1d":
                days = 1
                interval = "daily"
            elif period == "7d":
                days = 7
                interval = "daily"
            elif period == "1m":
                days = 30
                interval = "daily"
            elif period == "6m":
                days = 182
                interval = "daily"

            url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
            params = {"vs_currency": "usd", "days": days, "interval": interval}
            data = requests.get(url, params)

            if data is None or data.status_code != 200:
                error = "**O.O ocorreu um erro ao fazer a requisição**"
                await ctx.reply(content=error, ephemeral=True, mention_author=True)
                return

            data_values = data.json()
            prices = data_values["prices"]

            timestamps = [datetime.fromtimestamp(p[0] / 1000) for p in prices]
            values = [p[1] for p in prices]

            plt.figure(figsize=(10, 4))
            plt.plot(timestamps, values, color="gold", linewidth=2)
            plt.title(f"Preço do Bitcoin ({period})")
            plt.xlabel("Horário")
            plt.ylabel("USD")
            plt.grid(True)
            plt.tight_layout()
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m\n%H:%M"))
            plt.gcf().autofmt_xdate()
            plt.tight_layout()

            # Salvar em memória
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            plt.close()

            embed = discord.Embed(
                title=f"Gráfico do Bitcoin ({period})",
                color=discord.Color.gold()
            )

            file = discord.File(fp=buffer, filename="btc_graph.png")
            embed.set_image(url="attachment://btc_graph.png")

            await ctx.reply(embed=embed, file=file, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotCommands(bot))