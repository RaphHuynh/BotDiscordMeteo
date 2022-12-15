import discord
import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from discord.ext import commands
from discord import Color

api_key="your-key-api-openweathermap"
base_url="https://api.openweathermap.org/data/2.5/weather?"
base_url_forecast="https://api.openweathermap.org/data/2.5/forecast?"

client = commands.Bot(intents=discord.Intents.all() , command_prefix= "!" , description='The Best Bot For the Best User!')

@client.event
async def on_ready():
    print('connecter {}'.format(client.user.name)) 
    print('Bot ID: {}'.format(client.user.id))
    
@client.command(name="meteo")
async def meteo(ctx, city:str):
    city_name=city
    complete_url = base_url+"lang=fr&appid="+api_key+"&q="+city_name
    response = requests.get(complete_url)
    x = response.json()
    print(x)
    channel = ctx.message.channel
        
    if x["cod"] != "404":
        async with channel.typing():
            y = x['main']
            current_temperature= y['temp']
            current_temperature_celsius=str(round(current_temperature - 273.15))
            current_pression = y["pressure"]
            current_humidity = y["humidity"]
            z=x["weather"]
            icon=z[0]["icon"]
            weather_description=z[0]["description"]
            embed=discord.Embed(title=f"Météo dans {city_name}",color=0x4dff4d)
            embed.add_field(name="Description",value=f"**{weather_description}**")
            embed.set_thumbnail(url="https://openweathermap.org/img/wn/"+icon+"@2x.png")
            embed.add_field(name="Temperature(C)", value=f"**{current_temperature_celsius}°C**",inline="True")
            embed.add_field(name="Humidité(%)",value=f"**{current_humidity}%**",inline="False")
            embed.add_field(name="Pression Atmospherique(hPa)",value=f"**{current_pression}hPa**")
            embed.set_footer(text=f"Requête par {ctx.author.name}")
            await channel.send(embed=embed) 
    else:
        await channel.send("La ville n'existe pas !")

@client.command(name="previsionsemaine")
async def previsionsemaine(ctx, city:str):
    city_name=city
    complete_url = base_url_forecast+"lang=fr&appid="+api_key+"&q="+city_name
    reponse=requests.get(complete_url)
    x = reponse.json()
    print(x)
    channel = ctx.message.channel
    
    if x["cod"]!="404":
        async with channel.typing():
            y= x['list']
            for i in [0,8,16,24,32]:
                current_temp=y[i]['main']['temp']
                current_temp_cel=str(round(current_temp - 273.15))
                description=y[i]['weather'][0]['description']
                icon=y[i]['weather'][0]['icon']
                date=time.ctime(y[i]['dt'])
                list_temp=[]
                list_date_gmtime=[]
                list_date=[]
                embed=discord.Embed(title=f"Météo dans {city_name}",color=0x4dff4d)
                embed.add_field(name="Date :",value=f"**{date}**",inline=False)
                embed.add_field(name="Description",value=f"**{description}**")
                embed.add_field(name="Température :",value=f"**{current_temp_cel}**°C")
                embed.set_thumbnail(url="https://openweathermap.org/img/wn/"+icon+"@2x.png")
                for j in range(i,i+8):
                    current_temp=y[j]['main']['temp']
                    current_temp_cel=round(current_temp - 273.15)
                    list_temp.append(current_temp_cel)
                    date=time.gmtime(y[j]['dt'])
                    list_date_gmtime.append(date)
                    list_date.append(str(time.strftime("%-H",list_date_gmtime[j-i])))
                print(list_date)
                fig, ax = plt.subplots()
                ax.plot(list_date, list_temp, label="température")
                ax.set_xlabel("Heure (h)")
                ax.set_ylabel("Temp (Celsius)")
                ax.set_title("Température de la semaine")
                plt.legend()
                fig.savefig("/Users/huynh/Desktop/projet/botMeteo/bot-meteo/include//graphdemain.png")
                plt.close()
                
                file = discord.File("/Users/huynh/Desktop/projet/botMeteo/bot-meteo/include/graphdemain.png", filename="graphdemain.png")
                embed.set_footer(text=f"Requête par {ctx.author.name}")
                embed.set_image(url="attachment://graphdemain.png")
                    
                await channel.send(file=file,embed=embed) 
    else :
        await channel.send(embed=embed)
        
@client.command(name="meteodemain")
async def meteodemain(ctx, city:str):
    city_name=city
    complete_url = base_url_forecast+"lang=fr&appid="+api_key+"&q="+city_name
    reponse=requests.get(complete_url)
    x = reponse.json()
    print(x)
    channel = ctx.message.channel
    if x["cod"]!="404":
        async with channel.typing():
            y= x['list']
            list_temp=[]
            list_date_gmtime=[]
            list_date=[]
            for i in range(8,16):
                current_temp=y[i]['main']['temp']
                current_temp_cel=round(current_temp - 273.15)
                list_temp.append(current_temp_cel)
                date=time.gmtime(y[i]['dt'])
                list_date_gmtime.append(date)
                list_date.append(str(time.strftime("%-H",list_date_gmtime[i-8])))
            #graphe
                        
            fig, ax = plt.subplots()
            ax.plot(list_date, list_temp, label="température")
            ax.set_xlabel("Heure (h)")
            ax.set_ylabel("Temp (Celsius)")
            ax.set_title("Température de demain")
            plt.legend()
            fig.savefig("/Users/huynh/Desktop/projet/botMeteo/bot-meteo/include//graphdemain.png")
            plt.close()

            #creation card discord
            date_time=time.ctime(y[8]['dt'])
            icon=y[8]['weather'][0]['icon']
            description=y[8]['weather'][0]['description']
            file = discord.File("/Users/huynh/Desktop/projet/botMeteo/bot-meteo/include/graphdemain.png", filename="graphdemain.png")
            embed=discord.Embed(title=f"Météo dans {city_name}",color=0x4dff4d)
            embed.add_field(name="Date :",value=f"**{date_time}**",inline=False)
            embed.add_field(name="Description",value=f"**{description}**")
            embed.set_thumbnail(url="https://openweathermap.org/img/wn/"+icon+"@2x.png")
            embed.set_image(url="attachment://graphdemain.png")
            embed.set_footer(text=f"Requête par {ctx.author.name}")
            await channel.send(file=file,embed=embed) 
    else :
        await channel.send(embed=embed)
        
@client.command(name="meteoaujourdhui")
async def meteoaujourdui(ctx, city:str):
    city_name=city
    complete_url = base_url_forecast+"lang=fr&appid="+api_key+"&q="+city_name
    reponse=requests.get(complete_url)
    x = reponse.json()
    print(x)
    channel = ctx.message.channel
    if x["cod"]!="404":
        async with channel.typing():
            y= x['list']
            list_temp=[]
            list_date_gmtime=[]
            list_date=[]
            for i in range(0,8):
                current_temp=y[i]['main']['temp']
                current_temp_cel=round(current_temp - 273.15)
                list_temp.append(current_temp_cel)
                date=time.gmtime(y[i]['dt'])
                list_date_gmtime.append(date)
                list_date.append(str(time.strftime("%-H",list_date_gmtime[i])))
            #graphe
                        
            print(list_date)
            fig, ax = plt.subplots()
            ax.plot(list_date, list_temp, label="température")
            ax.set_xlabel("Heure (h)")
            ax.set_ylabel("Temp (Celsius)")
            ax.set_title("Température d'aujourd'hui")
            plt.legend()
            fig.savefig("/Users/huynh/Desktop/projet/botMeteo/bot-meteo/include//graphdemain.png")
            plt.close()

            #creation card discord
            date_time=time.ctime(y[8]['dt'])
            icon=y[8]['weather'][0]['icon']
            description=y[8]['weather'][0]['description']
            file = discord.File("/Users/huynh/Desktop/projet/botMeteo/bot-meteo/include/graphdemain.png", filename="graphdemain.png")
            embed=discord.Embed(title=f"Météo dans {city_name}",color=0x4dff4d)
            embed.add_field(name="Date :",value=f"**{date_time}**",inline=False)
            embed.add_field(name="Description",value=f"**{description}**")
            embed.set_thumbnail(url="https://openweathermap.org/img/wn/"+icon+"@2x.png")
            embed.set_image(url="attachment://graphdemain.png")
            embed.set_footer(text=f"Requête par {ctx.author.name}")
            await channel.send(file=file,embed=embed) 
    else :
        await channel.send(embed=embed)
        
@client.command(name="commands")
async def commands(ctx):
    channel = ctx.message.channel
    async with channel.typing():
        embed=discord.Embed(title="Commandes pour le bot",color=0x4dff4d)
        embed.add_field(name="!meteo Nom De la ville",value=f"Météo actuel dans la ville.",inline=False)
        embed.add_field(name="!meteoaujourdhui Nom De La Vile", value="Météo d'aujourd'hui sous 24h", inline=False)
        embed.add_field(name="!meteodemain Nom de la ville",value=f"Météo pour demain de la ville demandée.",inline=False)
        embed.add_field(name="!previsionsemaine Nom de la ville",value=f"Prevision des 5 prochains jours de la ville demandée.",inline=False)
        embed.set_footer(text=f"Requête par {ctx.author.name}")
        await channel.send(embed=embed) 

#mettre le token de ton bot discord
client.run("your-token")