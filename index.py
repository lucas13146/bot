#---------[Assets]--------#
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

owner_id = os.getenv('OWNER_ID')
prefix = os.getenv('PREFIX')
token = os.getenv('TOKEN')

intents = discord.Intents(messages=True, guilds=True, members=True)
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True
intents.all()

client = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

#---------[Ready]--------#

@client.event
async def on_ready():
    os.system('cls')
    print("Le bot est on ...")
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"{prefix}help"))

#---------[Ping]--------#

@client.command(name="ping")
async def ping(ctx):
    if(ctx):
        await ctx.message.delete()

    em = discord.Embed(
        title=f"Pong",
        color=discord.Color.from_rgb(255, 85, 85)
    )

    await ctx.send(embed=em)

#---------[reaction-role]--------#

msg_reaction = []

@client.command(name="reaction-role")
async def reaction(ctx):
    if(ctx):
        await ctx.message.delete()

    em = discord.Embed(
        title=f"Reaction Role :",
        description=f"Jaune : `🟡` \n\n Rouge : `🔴`",
        color=discord.Color.from_rgb(255, 85, 85)
    )

    message = await ctx.send(embed=em)
    await message.add_reaction("🟡")
    await message.add_reaction("🔴")
    msg_reaction.append(message.id)

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(message_id)
    guild_id = payload.guild_id
    user = payload.member
    guild = client.get_guild(guild_id)

    if message_id in msg_reaction:
        if payload.emoji.name == "🟡":
            if payload.user_id != client.user.id:
                role_jaune = guild.get_role(878980986875043910)
                await user.add_roles(role_jaune)
                await message.remove_reaction("🟡", user)

        if payload.emoji.name == "🔴":
            if payload.user_id != client.user.id:
                role_rouge = guild.get_role(878981055330271252)
                await user.add_roles(role_rouge)
                await message.remove_reaction("🔴", user)

#---------[on_member_join]--------#

@client.event
async def on_member_join(member):
    channel = client.get_channel(878972029670420542)
    await channel.send(f"Le joueur `{member.name}` a rejoint le serveur ...")

#---------[Login]--------#
def run():
    client.run(token)

run()
