import os
import discord
from discord import app_commands
from discord.ext import commands
from discord import DMChannel
from discord.ext.commands import has_permissions, MissingPermissions
from keep_alive import keep_alive
from discord.ext import tasks
from itertools import cycle
import requests
import datetime
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", case_insensitive=True, intents=intents)
cats = ["idk", "idfk"]

@bot.event
async def on_ready():
    change_status.start()
    print("Bot is ready!")
    await schedule_events()
    try:
        synced = await bot.tree.sync()
        print(f"Synced{len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    msg = message.content

    if message.author == bot.user:
        return
  
    if 'stfu' in message.content.lower():
        await message.delete()
      
    if 'iran' in message.content.lower():
        await message.delete()
      
    if 'dog' in msg.lower():
        await message.channel.send("yeahhh")

    if 'loch' in msg.lower():
        await message.channel.send("lochlann sucks")

    if 'lach' in msg.lower():
        await message.channel.send("fuck u")

    #if 'hello' in msg.lower():
        #await message.channel.send("Hello! How may I assist you?")
    
    #if 'hi' in msg.lower():
        #await message.channel.send("Hello! How may I assist you?")

    if 'iris' in msg.lower():
        await message.channel.send('iris is the best!!!')

    if 'ian' in msg.lower():
        await message.channel.send(":D")

    await bot.process_commands(message)
  

@bot.command(name='hello', aliases=['hi', 'hey', 'wassup'], description='HI!!!')
async def hello(ctx):
    await ctx.channel.send("Hi! I'm BOT. I'm still in development, but I recieve updates frequently!")


@bot.command(name='helpme', aliases=['saveme', 'what', 'plshelp'], description='idk')
async def helpme(ctx):
    await ctx.send("Here are some features you can use: /desc   /status ")

@bot.command(name='ver', aliases=['version'], description='ver!')
async def ver(ctx):
    await ctx.send("The current version: 1.2.3")

@bot.command(name='stats', aliases=['status'], description='stats!')
async def stats(ctx):
    await ctx.send("Last updated 7/26/2023 ")

@bot.command(name='desc', aliases=['description', 'wtfisthis'], description='wat this is')
async def desc(ctx):
    await ctx.send("Created by Ian and Iris to make a bot because they were bored. Created 3/1/2023 ")

@bot.command(name='cat', aliases=['catsrbetter', 'cats>dogs', 'dogs<cats'], description='tells u why dogs r better', pass_context=True)
async def cats(ctx):
    usermember = ctx.message.author
    username = usermember.name
    message = [f'Hi {username}! u suck. imagine liking cats.\n\n[have sum dogs](https://www.pexels.com/search/dog/)\n\n dogs r cuter than ur face']

    embed = discord.Embed(
        title = 'fuk u',

       description = ''.join(message),

       color = discord.Color.red()
    )

    await DMChannel.send(usermember, embed=embed)
  
@bot.command(name='info', aliases=['information', 'abt', 'wtf'], description='idk', pass_context=True)
async def info(ctx):
    embed = discord.Embed(description="Some bot information.", color=000000)
    embed.set_author(name="BOT")
    embed.set_thumbnail(url="https://i.imgur.com/1OZ6aHg.png")
    embed.add_field(name="Developer", value="Iris and Ian", inline=True)
    embed.add_field(name="Version", value="1.2.3", inline=True)
    await ctx.send(embed=embed)

@bot.command(name='begone', aliases=['clear', 'del'], description='Deletes multiple messages at once.', pass_context=True)
async def clear(ctx, amount=0):
    if amount<=100:
      await ctx.channel.purge(limit=amount+1)
    else:
      await ctx.send("You cannot delete more than 100 messages at a time.")
    return

@clear.error
async def clear_error(error, ctx):
   if isinstance(error, MissingPermissions):
       await ctx.send("You are not an Admin!")
     
@bot.event
async def on_member_join(member):
    guild = member.guild
    print(f"Guild name: {guild.name}")
    role = discord.utils.get(member.guild.roles, name="tester")
    welcome_channel = discord.utils.get(guild.text_channels, name="welcome")
    welcome_message = f"Welcome to the server, {member.mention}!"
    await welcome_channel.send(welcome_message)
    
    welcome_embed = discord.Embed(title='Hi!', description=' This server is used for testing our BOT. Read the rules and we hope you enjoy! (btw this bot is completely forked off of bills code so he gets all the credit)')
    await member.send(embed=welcome_embed)

    await member.add_roles(role, reason="Testing role assignment")

@bot.command(name='dogs', aliases=['dog', 'doggo'], description='dogs!!!', pass_context=True)
async def embed_thing(ctx):
    message = "```\n           __\n      (___()'`;\n      /,    /`\njgs   \\\"--\\\"\n```"
    additional_message = "dogs are great\n\n"
    embed_thing = discord.Embed(title='YEAHHH DOGS', description=additional_message + message)
    await ctx.send(embed=embed_thing)

@bot.tree.command(name="face", description="face!")
async def face(interaction: discord.Interaction):
    await interaction.response.send_message("ur face")  

@bot.tree.command(name="say", description="ughhh")
async def say(interaction: discord.Interaction, thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.display_name} said: '{thing_to_say}'")

def fetch_random_cat_fact():
    url = "https://cat-fact.herokuapp.com/facts/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        fact = data["text"]
        return fact
    else:
        return "u have failed"

#@bot.tree.command(name="catfact")
#async def catfact(interaction: discord.Interaction):
   # fact = fetch_random_cat_fact()
    #await interaction.response.send_message(f"Here's an interesting cat fact:\n{fact}")

@bot.tree.command(name="catfact", description="have sum cat facts")
async def catfact(interaction: discord.Interaction):
    fact = fetch_random_cat_fact()
    await interaction.response.send_message("Here's an interesting cat fact:\ncats are cute")

def fetch_random_dog_image():
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        image_url = data["message"]
        return image_url
    else:
        return "u have failed"

@bot.tree.command(name="dogpic", description="have a dog pic!")
async def dogpic(interaction: discord.Interaction):
    image_url = fetch_random_dog_image()
    if image_url:
        await interaction.response.send_message(image_url)
    else:
        await interaction.response.send_message("ur dog image fetching has failed")

import random

images = [
    "https://media.discordapp.net/attachments/1102814861697761310/1118789919075213362/20230610_173008.jpg?width=883&height=662",
  "https://media.discordapp.net/attachments/1102814861697761310/1118789919461081088/20230610_120944.jpg?width=496&height=662",
    "https://media.discordapp.net/attachments/1102814861697761310/1118789919956025385/20230610_115207.jpg?width=496&height=662",
    "https://media.discordapp.net/attachments/1102814861697761310/1118789920346087485/20230610_110946.jpg?width=883&height=662",

"https://media.discordapp.net/attachments/1102814861697761310/1118791458149896192/IMG-20230610-WA0007.jpg?width=308&height=662",

"https://media.discordapp.net/attachments/1102814861697761310/1118791458414133300/20230402_145635.jpg?width=496&height=662",

"https://media.discordapp.net/attachments/1102814861697761310/1118791458690969671/20230402_144147.jpg?width=496&height=662",

"https://media.discordapp.net/attachments/1102814861697761310/1118791458988757022/mmexport1679964524801.jpg?width=883&height=662",

"https://media.discordapp.net/attachments/1102814861697761310/1118791459278159982/mmexport1679964340689.jpg?width=646&height=662",
]

@bot.tree.command(name="dingus", description="doggo")
async def dingus(interaction: discord.Interaction):
    chosen_image = random.choice(images)
    await interaction.response.send_message(chosen_image)

@bot.tree.command(name="catgirl", description="Φ ω Φ")
async def catgirl(interaction: discord.Interaction):
    image_url = await fetch_random_catgirl_image()
    if image_url:
        await interaction.response.send_message(image_url)
    else:
        await interaction.response.send_message("u failed")

async def fetch_random_catgirl_image():
    try:
        response = requests.get("https://api.waifu.pics/sfw/neko")
        if response.status_code == 200:
            data = response.json()
            image_url = data["url"]
            return image_url
        else:
            print(f"failed to fetch ur catgirl. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"error fetching ur image: {e}")
        return None


import json

with open("dudes.json", "r") as file:
    data = json.load(file)
    hotguy = data["images"]

@bot.tree.command(name="hotdude", description="hot dudes!")
async def hotdude(interaction: discord.Interaction):
    chosen_image = random.choice(hotguy)
    await interaction.response.send_message(chosen_image)

async def send_msg(event_message):
    channel = bot.get_channel(1140554432073973861)
    await channel.send(event_message)

async def schedule_events():
    while True:
        current_date = datetime.datetime.now().date()
        target_date = datetime.date(current_date.year, 8, 16)

        if current_date == target_date:
            await send_msg("dogs!")

        await asyncio.sleep(86400)
      
status = cycle(['with Python','JetHub'])

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

url = "https://discord.com/api/v10/applications/<my_application_id>/guilds/<guild_id>/commands"
# This is an example USER command, with a type of 2
json = {
    "name": "High Five",
    "type": 2
}
# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot <my_bot_token>"
}
# or a client credentials token for your app with the applications.commands.update scope
headers = {
    "Authorization": "Bearer <my_credentials_token>"
}
r = requests.post(url, headers=headers, json=json)
  
keep_alive()
my_secret = os.environ['bot_1']
bot.run(my_secret)





