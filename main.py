import discord, os
from discord.ext import commands
import requests 
import keygen
from server import run 
from threading import Thread


api = "https://automatic-auth-bot.ryanservices69.repl.co"
tkn = "MTEzMDkyMjA0NzM0MjY0MTI4Mw.GNxIDd.8nY_83iwhUi9uNfCq7eHl3OCZENDlp3ZObfAlY"
offline_token = "MTEyMjEyNzIyMzE3NzA4OTEwNA.GGrpC9.aZWYEMlcdidZPpDrzWXVnlGw-uAcruXGfz9n7Q"
online_token = "MTEyMjE1OTQzOTQyODk4MDczNg.GBSZ1v.1gtcMPnktYB0ZLfCKqc--3e13vOi5pyMj2ZnYM"

client = commands.Bot(command_prefix=(["-", "."]), intents=discord.Intents.all())

@client.event
async def on_ready():
    os.system("clear||cls")
    print("connected;", client.user)
    

@client.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound):
        return
    em = discord.Embed(title="Error", description=f"```{error}```", color=00000)
    await ctx.send(embed=em)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def status(ctx, guild_id= None):
    msg = await ctx.send("Fetching.....")
    if guild_id == None:
        f = open("running.txt", "r").read().splitlines()
        if len(f) == 0:
            return await msg.edit(content="No running tasks.")
        embed = discord.Embed(title="Running Tasks", description="", color=00000)
        for guild in f:
            # print(type(guild))
            total = open("guilds/"+guild+"-total.txt", "r").read()
            added = open("guilds/"+guild+".txt", "r").read()
            # print(total, added)
            remaining = int(total) - int(added)
            speed_per_minute = 60
            estimated_minutes = int(remaining) / speed_per_minute
            hours = int(estimated_minutes / 60)
            minutes = int(estimated_minutes % 60)
            seconds = int((estimated_minutes % 1) * 60)
            if hours > 0:
                estimated_time = f"{hours}h {minutes}m {seconds}s"
            else:
                estimated_time = f"{minutes}m {seconds}s"
            added_percent = int((int(added) / int(total)) * 100)
            remaining_percent = int((int(remaining) / int(total)) * 100)
            embed.description += f"Guild: `{guild}`\nAdded: `{added}/{total} {added_percent}%`\nRemaining: `{remaining} {remaining_percent}%`\nSpeed: `60/m`\nETA: `{estimated_time}`\n\n"
        await ctx.send(embed=embed)
    else:
            f = open("running.txt", "r").read().splitlines()
            if guild_id not in f:
                return await ctx.send("No Running task found for guild: " + guild_id)
            else:
                total = open("guilds/"+guild_id+"-total.txt", "r").read()
                added = open("guilds/"+guild_id+".txt", "r").read()
                remaining = int(total) - int(added)
                speed_per_minute = 60
                estimated_minutes = int(remaining) / speed_per_minute
                hours = int(estimated_minutes / 60)
                minutes = int(estimated_minutes % 60)
                seconds = int((estimated_minutes % 1) * 60)
                if hours > 0:
                    estimated_time = f"{hours}h {minutes}m {seconds}s"
                else:
                    estimated_time = f"{minutes}m {seconds}s"
                added_percent = int((int(added) / int(total)) * 100)
                remaining_percent = int((int(remaining) / int(total)) * 100)
                em = discord.Embed(title=f"Status - {guild_id}", description="", color=00000)
                em.description += f"Guild: `{guild_id}`\nAdded: `{added}/{total} {added_percent}%`\nRemaining: `{remaining} {remaining_percent}%`\nSpeed: `60/m`\nETA: `{estimated_time}`\n\n"
                await ctx.send(embed=em)

        
@client.command(aliases=['gen'])
async def generate(ctx, key_type:str, start:int, total:int, uses=None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("unauthorized")
    if "ryan" not in ctx.author.name.lower():
        return await ctx.send("unauthorized")
    key, url = keygen.generate_key(key_type=key_type, total=total, start=start, uses=uses)
    em = discord.Embed(title="Key Generated", description=f"Key: `{key}`\nType: `{key_type}`\nAmount: `{total}`\n\nBot Invite: [Click here to Invite]({url})\n\nNote: ```It will start automatically as soon as you add the bot, if didn't start make sure the bot is in server and send command .redeem```", color=00000)
    await ctx.send(embed=em)
    
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def redeem(ctx, key=None, server_id=None):
    if key == None or server_id == None:
        return await ctx.send("usage: .redeem <key> <server-id>")
    url = f"{api}/callback?code=ded&state={key}&guild_id={server_id}&permissions=1"
    r = requests.get(url)
    if "success" not in r.json() and "invalid" not in r.json():
        await ctx.message.delete()
    em = discord.Embed(description=f"{r.json()}", color=00000)
    return await ctx.send(embed=em)

@client.command()
async def ltc(ctx): 
    await ctx.send("LeUUjdR44S9314Y3LQUW1JeS4HCsDt6mK1")
    await ctx.send("ltc addy ^^")

@client.command()
async def mail(ctx): 
    await ctx.send("**requested1337@protonmail.com**")
    await ctx.send("Coinbase / Binance mail ^")

@client.command()
async def upi(ctx):
    await ctx.send("ping owner")

@client.command()
async def calc(ctx, *, expression):
    sol = eval(expression)
    await ctx.send(f"{expression} = {sol}")

@client.command()
async def ping(ctx):
    await ctx.send(f"{round(client.latency * 1000)}ms")

@client.command()
async def vt(ctx, *, vouch):
    msg = await ctx.send(f"`+rep <@468818639588687873> {vouch}`")
    await msg.reply("> copy paste this in <#1119597593048121404> channel.")

@client.command()
async def leave(ctx, type:str, guild: str):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("unauthorized")
    if "ryan" not in ctx.author.name.lower():
        return await ctx.send("unauthorized")
    if type == "offline": 
        # remove_tracking(guild)
        r = requests.delete("https://canary.discord.com/api/v9/users/@me/guilds/"+guild, headers={"Authorization": "Bot "+offline_token})
        em = discord.Embed(description=f"{r.json()}", color=00000)
        return await ctx.send(embed=em)
    elif type == "online":
        r = requests.delete("https://canary.discord.com/api/v9/users/@me/guilds/"+guild, headers={"Authorization": "Bot "+online_token})
        em = discord.Embed(description=f"{r.json()}", color=00000)
        return await ctx.send(embed=em)
    else:
        return await ctx.send("Invalid type, type can be either offline or online.")

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def stock(ctx):
    offline = len(open("offline.txt", "r").read().splitlines())
    online = len(open("online.txt", "r").read().splitlines())
    em = discord.Embed(title="Stock", description=f"Offline: `{offline}`\nOnline: `{online}`", color=00000)
    await ctx.send(embed=em)
Thread(target=run).start()
client.run(tkn)