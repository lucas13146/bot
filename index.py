#----------------[Assets]----------------#
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingRequiredArgument, MissingPermissions
import os
import sys
import json
import asyncio

prefix = "-"
token = "ODUwMzkwMDQ0ODMyNDMyMTU5.YLpBcg.n7hGMxXnm-oXaRkkrwThONZk-l8"

client = commands.Bot(command_prefix=prefix, help_command=None)

#----------------[Ready]----------------#

temp_channel_id = None

async def get_temp_channel():
    with open(f"bdd/temp.json", "r") as f:
        channel = json.load(f)

    return channel


async def open_temp_channel(channel):
    data = await get_temp_channel()

    data["channel"] = int(channel.id)

    with open(f"bdd/temp.json", "w") as f:
        json.dump(data, f)

    return True

@client.event
async def on_ready():
    print("Bot connected ...")
    data = await get_temp_channel()
    if data["channel"] != 0:
        channel_id = data["channel"]
        chnl = client.get_channel(channel_id)
        await chnl.send("Bot online ...")
        data["channel"] = 0
        with open(f"bdd/temp.json", "w") as f:
            json.dump(data, f)

#----------------[Owner]----------------#

async def get_permision_members():
    with open(f"bdd/perm.json", "r") as f:
        channel = json.load(f)

    return channel


async def open_permision_account(member, perm):
    data = await get_permision_members()

    if str(member.id) in data:
        return False
    else:
        data[str(member.id)] = perm

    with open(f"bdd/perm.json", "w") as f:
        json.dump(data, f)

    return True

@client.command(name="set_owner")
async def set_owner(ctx, member:discord.Member = None):
    guild = ctx.guild
    if member == None:
        member = ctx.author
    else:
        member = member
    
    if member.id == 560849136899850261:
        await open_permision_account(member, "owner")

        msg = await ctx.send(f"Les permision de owner on bien été ajouté à : **{member.name}**")
        await asyncio.sleep(4)
        await msg.delete()
    else:
        msg = await ctx.send("Tu a pas la permision de fair sa ...")
        await asyncio.sleep(4)
        await msg.delete()

#----------------[Restart]----------------#

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.command()
async def restart(ctx):
    data_perm = await get_permision_members()
    if (data_perm):
        if str(ctx.author.id) in data_perm:
            await ctx.message.delete()
            message = await ctx.send("Restarting...")
            temp_channel = ctx.channel
            await open_temp_channel(temp_channel)
            restart_program()
        else:
            msg = await ctx.send("Tu a pas la permision de fair sa ...")
            await asyncio.sleep(4)
            await msg.delete()
    else:
        msg = await ctx.send("Tu a pas la permision de fair sa ...")
        await asyncio.sleep(4)
        await msg.delete()

#----------------[Clear]----------------#

@client.command(name="clear", pass_content=True)
@has_permissions(manage_messages=True)
async def clear(ctx, number):
    await ctx.channel.purge(limit=int(number) + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(
            title="❌Il y a une erreur :",
            description="Vous avez pas la permission de fair sa !",
            color=discord.Color.from_rgb(47, 49, 54)
        )
        await ctx.send(embed=embed)
    if isinstance(error, MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Mauvaise utilisation de la commande.",
            description=f"`{prefix}clear <nombre>`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

#----------------[Login]----------------#

def run():
    client.run(token)

run()