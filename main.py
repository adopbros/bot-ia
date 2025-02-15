import discord
from discord.ext import commands
import os,random
import requests
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def meme(ctx):
    image = os.listdir("images")
    img_name = random.choice(image)
    with open(f'images/{img_name}', 'rb') as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)

@bot.command('duck')
async def duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attchment in ctx.message.attachments:
            file_name = attchment.filename
            file_url = attchment.url
            await attchment.save(file_name)
            await ctx.send("archivo guardado correctamente")

            try:
                class_name = get_class("keras_model.h5", "labels.txt", file_name)

                if class_name[0] == "personas":
                    await ctx.send("esto es una persona puede pasar")
                elif class_name[0] == "perros":
                    await ctx.send("esto es un perro no puede pasar")

            except:
                await ctx.send("esto no es ni perro ni humano o revisa el formato de imegen y cambialo")


    else:
        await ctx.send("olvidaste subir una imagen")


bot.run("token")