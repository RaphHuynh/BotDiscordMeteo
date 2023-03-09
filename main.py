import discord
import time
import matplotlib.pyplot as plt
import requests

from config import *

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Bot is connect")


@bot.slash_command(
    description="liste des commandes",
    name="command"
)
async def command(ctx):
    embed = discord.Embed(
        title="Liste commandes",
        description="Liste des commandes du bot",
        color=discord.Colour.dark_blue()

    )
    embed.add_field(name="/meteo", value="Commande pour donner la météo en directe d'une ville.", inline=False)
    embed.add_field(name="/prevision", value="Prévision de la météo sur 24h.", inline=False)
    embed.add_field(name="/prevision-demain", value="Prévision de la météo de demain", inline=False)
    embed.add_field(name="/prevision-semaine", value="Prévision sur 5 jours", inline=False)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/6428/6428802.png")
    embed.set_footer(text="RaynhCoding")

    await ctx.respond(embed=embed)


@bot.slash_command(
    name="meteo",
    description="Meteo actuel de la ville."
)
async def meteo(ctx, ville: discord.Option(str, 'ville', required=True)):
    complete_url = BASE_URL + "lang=fr&appid=" + API + "&q=" + ville
    response = requests.get(complete_url)
    response = response.json()

    if response["cod"] != "404":
        response_main = response['main']
        current_temperature = response_main['temp']
        current_temperature = str(round(current_temperature - 273.15))
        current_pressure = response_main['pressure']
        current_humidity = response_main['humidity']
        response_weather = response["weather"]
        icon = response_weather[0]['icon']
        weather_description = response_weather[0]["description"]
        embed = discord.Embed(
            title=f"Météo de {ville}",
            color=discord.Colour.dark_blue()
        )
        embed.add_field(name="Description", value=f"{weather_description}")
        embed.add_field(name="Température", value=f"{current_temperature} °C", inline=True)
        embed.add_field(name="Humidité", value=f"{current_humidity} %", inline=False)
        embed.add_field(name="Pression Atmospherique", value=f"{current_pressure} hPa")
        embed.set_thumbnail(url="https://openweathermap.org/img/wn/" + icon + "@2x.png")
        embed.set_footer(text="Par RaynhCoding")

        await ctx.respond(embed=embed)
    else:
        await ctx.respond("La ville n'existe pas.")


@bot.slash_command(
    name="prevision",
    description="Prévision de la température du jour"
)
async def prevision(ctx, ville: discord.Option(str, 'ville', required=True)):
    complete_url = BASE_URL_FORECAST + "lang=fr&appid=" + API + "&q=" + ville
    response = requests.get(complete_url)
    response = response.json()

    if response["cod"] != "404":
        response_list = response['list']
        temp_list = []
        date_gm_list = []
        date_list = []

        for i in range(0, 8):
            temp_current = response_list[i]['main']['temp']
            temp_current = round(temp_current - 273.15)
            temp_list.append(temp_current)
            date_gm_list.append(time.gmtime(response_list[i]['dt']))
            date_list.append(str(time.strftime("%-H", date_gm_list[i])))

        # graphe

        fig, ax = plt.subplots()
        ax.plot(date_list, temp_list, label="température")
        ax.set_xlabel("Heure (h)")
        ax.set_ylabel("Température (Celsius")
        ax.set_title("Température du jour")
        plt.legend()
        fig.savefig("./graphdemain.png")
        plt.close()

        # create embed

        date_time = time.ctime(response_list[8]['dt'])
        icon = response_list[0]['weather'][0]['icon']
        description = response_list[0]['weather'][0]['description']
        file = discord.File("./graphdemain.png", filename="graphdemain.png")
        embed = discord.Embed(
            title=f"Prévision de {ville}",
            color=discord.Colour.dark_blue()
        )
        embed.add_field(name="Date :", value=f"{date_time}", inline=False)
        embed.add_field(name="Description :", value=f"{description}")
        embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")
        embed.set_image(url="attachment://graphdemain.png")
        embed.set_footer(text="Par RaynhCoding")

        await ctx.respond(file=file, embed=embed)
    else:
        await ctx.respond("La ville n'existe pas.")


@bot.slash_command(
    name="prevision-demain",
    description="Prévision de demain"
)
async def prevision_demain(ctx, ville: discord.Option(str, 'ville', required=True)):
    complete_url = BASE_URL_FORECAST + "lang=fr&appid=" + API + "&q=" + ville
    response = requests.get(complete_url)
    response = response.json()

    if response["cod"] != "404":
        response_list = response['list']
        temp_list = []
        date_gm_list = []
        date_list = []

        for i in range(8, 16):
            temp_current = response_list[i]['main']['temp']
            temp_current = round(temp_current - 273.15)
            temp_list.append(temp_current)
            date_gm_list.append(time.gmtime(response_list[i - 8]['dt']))
            date_list.append(str(time.strftime("%-H", date_gm_list[i - 8])))

        # graphe

        fig, ax = plt.subplots()
        ax.plot(date_list, temp_list, label="température")
        ax.set_xlabel("Heure (h)")
        ax.set_ylabel("Température (Celsius")
        ax.set_title("Température du jour")
        plt.legend()
        fig.savefig("./graphdemain.png")
        plt.close()

        # create embed

        date_time = time.ctime(response_list[8]['dt'])
        icon = response_list[8]['weather'][0]['icon']
        description = response_list[8]['weather'][0]['description']
        file = discord.File("./graphdemain.png", filename="graphdemain.png")
        embed = discord.Embed(
            title=f"Prévision de {ville}",
            color=discord.Colour.dark_blue()
        )
        embed.add_field(name="Date :", value=f"{date_time}", inline=False)
        embed.add_field(name="Description :", value=f"{description}")
        embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")
        embed.set_image(url="attachment://graphdemain.png")
        embed.set_footer(text="Par RaynhCoding")

        await ctx.respond(file=file, embed=embed)
    else:
        await ctx.respond("La ville n'existe pas")


@bot.slash_command(
    name="prevision-semaine",
    description="Prévision de la semaine"
)
async def prevision_semaine(ctx, ville: discord.Option(str, 'ville', required=True)):
    complete_url = BASE_URL_FORECAST + "lang=fr&appid=" + API + "&q=" + ville
    response = requests.get(complete_url)
    response = response.json()

    if response["cod"] != "404":
        response = response['list']

        for i in [0, 8, 16, 24, 32]:
            temp_current = response[i]['main']['temp']
            temp_current = str(round(temp_current - 273.15))
            description = response[i]['weather'][0]['description']
            icon = response[i]['weather'][0]['icon']
            date = time.ctime(response[i]['dt'])
            temp_list = []
            date_gm_list = []
            date_list = []

            # card embed

            embed = discord.Embed(
                title=f"Météo dans {ville}",
                color=discord.Colour.dark_blue()
            )
            embed.add_field(name="Date :", value=f"{date}", inline=False)
            embed.add_field(name="Description", value=f"{description}")
            embed.add_field(name="Température", value=f"{temp_current}")
            embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")

            for j in range(i, i + 8):
                temp_current = response[j]['main']['temp']
                temp_current = round(temp_current - 273.15)
                temp_list.append(temp_current)
                date = time.gmtime(response[j]['dt'])
                date_gm_list.append(date)
                date_list.append(str(time.strftime("%-H", date_gm_list[j - i])))
            fig, ax = plt.subplots()
            ax.plot(date_list, temp_list, label="température")
            ax.set_xlabel("Heure (h)")
            ax.set_ylabel("Temp (Celsius)")
            ax.set_title("Température de la semaine")
            plt.legend()
            fig.savefig("./graphdemain.png")
            plt.close()

            file = discord.File("./graphdemain.png", filename="graphdemain.png")
            embed.set_footer(text="Par RaynhCoding")
            embed.set_image(url="attachment://graphdemain.png")

            await ctx.respond(file=file, embed=embed)
    else:
        await ctx.respond("La ville n'existe pas.")


bot.run(TOKEN)
