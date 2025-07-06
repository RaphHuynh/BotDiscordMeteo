import discord
import time
import matplotlib.pyplot as plt
import requests

from config import TOKEN, API, BASE_URL, BASE_URL_FORECAST

# Configuration des intents pour pycord
intents = discord.Intents.default()
intents.message_content = True

# Création du bot avec les intents
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")
    print(f"ID du bot: {bot.user.id}")
    print("Le bot est prêt à être utilisé !")


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
async def meteo(ctx, ville: str):
    """Affiche la météo actuelle d'une ville."""
    try:
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
            await ctx.respond("❌ La ville n'existe pas ou n'a pas été trouvée.")
    except Exception as e:
        await ctx.respond(f"❌ Une erreur s'est produite : {str(e)}")


@bot.slash_command(
    name="prevision",
    description="Prévision de la température du jour"
)
async def prevision(ctx, ville: str):
    """Affiche la prévision météo du jour avec graphique."""
    try:
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

            # Création du graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(date_list, temp_list, label="Température", marker='o', linewidth=2)
            ax.set_xlabel("Heure (h)")
            ax.set_ylabel("Température (°C)")
            ax.set_title(f"Prévision de température pour {ville}")
            ax.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            fig.savefig("./graphdemain.png", dpi=300, bbox_inches='tight')
            plt.close()

            # Création de l'embed
            date_time = time.ctime(response_list[0]['dt'])
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
            await ctx.respond("❌ La ville n'existe pas ou n'a pas été trouvée.")
    except Exception as e:
        await ctx.respond(f"❌ Une erreur s'est produite : {str(e)}")


@bot.slash_command(
    name="prevision-demain",
    description="Prévision de demain"
)
async def prevision_demain(ctx, ville: str):
    """Affiche la prévision météo de demain avec graphique."""
    try:
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
                date_gm_list.append(time.gmtime(response_list[i]['dt']))
                date_list.append(str(time.strftime("%-H", date_gm_list[i - 8])))

            # Création du graphique
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(date_list, temp_list, label="Température", marker='o', linewidth=2)
            ax.set_xlabel("Heure (h)")
            ax.set_ylabel("Température (°C)")
            ax.set_title(f"Prévision de température pour demain - {ville}")
            ax.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            fig.savefig("./graphdemain.png", dpi=300, bbox_inches='tight')
            plt.close()

            # Création de l'embed
            date_time = time.ctime(response_list[8]['dt'])
            icon = response_list[8]['weather'][0]['icon']
            description = response_list[8]['weather'][0]['description']
            file = discord.File("./graphdemain.png", filename="graphdemain.png")
            embed = discord.Embed(
                title=f"Prévision de demain - {ville}",
                color=discord.Colour.dark_blue()
            )
            embed.add_field(name="Date :", value=f"{date_time}", inline=False)
            embed.add_field(name="Description :", value=f"{description}")
            embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")
            embed.set_image(url="attachment://graphdemain.png")
            embed.set_footer(text="Par RaynhCoding")

            await ctx.respond(file=file, embed=embed)
        else:
            await ctx.respond("❌ La ville n'existe pas ou n'a pas été trouvée.")
    except Exception as e:
        await ctx.respond(f"❌ Une erreur s'est produite : {str(e)}")


@bot.slash_command(
    name="prevision-semaine",
    description="Prévision de la semaine"
)
async def prevision_semaine(ctx, ville: str):
    """Affiche la prévision météo sur 5 jours avec graphiques."""
    try:
        complete_url = BASE_URL_FORECAST + "lang=fr&appid=" + API + "&q=" + ville
        response = requests.get(complete_url)
        response = response.json()

        if response["cod"] != "404":
            response = response['list']
            
            # Envoi du premier message pour indiquer le traitement
            await ctx.respond(f"🔄 Génération des prévisions pour {ville}...")

            for day_index, i in enumerate([0, 8, 16, 24, 32]):
                if i >= len(response):
                    break
                    
                temp_current = response[i]['main']['temp']
                temp_current = str(round(temp_current - 273.15))
                description = response[i]['weather'][0]['description']
                icon = response[i]['weather'][0]['icon']
                date = time.ctime(response[i]['dt'])
                temp_list = []
                date_gm_list = []
                date_list = []

                # Création de l'embed pour ce jour
                embed = discord.Embed(
                    title=f"Météo dans {ville} - Jour {day_index + 1}",
                    color=discord.Colour.dark_blue()
                )
                embed.add_field(name="Date :", value=f"{date}", inline=False)
                embed.add_field(name="Description", value=f"{description}")
                embed.add_field(name="Température", value=f"{temp_current} °C")
                embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{icon}@2x.png")

                # Données pour le graphique de ce jour
                for j in range(i, min(i + 8, len(response))):
                    temp_current_graph = response[j]['main']['temp']
                    temp_current_graph = round(temp_current_graph - 273.15)
                    temp_list.append(temp_current_graph)
                    date = time.gmtime(response[j]['dt'])
                    date_gm_list.append(date)
                    date_list.append(str(time.strftime("%-H", date_gm_list[j - i])))
                
                # Création du graphique
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(date_list, temp_list, label="Température", marker='o', linewidth=2)
                ax.set_xlabel("Heure (h)")
                ax.set_ylabel("Température (°C)")
                ax.set_title(f"Température du jour {day_index + 1} - {ville}")
                ax.grid(True, alpha=0.3)
                plt.legend()
                plt.tight_layout()
                fig.savefig("./graphdemain.png", dpi=300, bbox_inches='tight')
                plt.close()

                file = discord.File("./graphdemain.png", filename="graphdemain.png")
                embed.set_footer(text="Par RaynhCoding")
                embed.set_image(url="attachment://graphdemain.png")

                # Envoi de chaque jour comme message de suivi
                await ctx.followup.send(file=file, embed=embed)
        else:
            await ctx.respond("❌ La ville n'existe pas ou n'a pas été trouvée.")
    except Exception as e:
        await ctx.respond(f"❌ Une erreur s'est produite : {str(e)}")


bot.run(TOKEN)
