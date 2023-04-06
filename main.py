import discord
from discord.ext import commands

intents = discord.Intents().all()  # or specify the intents you want to use
bot = commands.Bot(command_prefix='!', intents=intents)

# define a command to send a welcome message to new members
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Welcome {member.mention} to the server!')

# define a command to send a greeting message when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready to go!')

# define a command to respond to a user command
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')


@bot.command(name='kick')
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member from the server."""
    await member.kick(reason=reason)
    await ctx.send(f'Member {member} has been kicked.')

@bot.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a member from the server."""
    await member.ban(reason=reason)
    await ctx.send(f'Member {member} has been banned.')

@bot.command(name='echo')
async def echo(ctx, *, message):
    """Echoes the user's message."""
    await ctx.send(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong!')

@bot.command(name='info')
async def info(ctx):
    embed=discord.Embed(title="FatCisBot OSC", description="FatCisBot OSC (OSC = Open Source Core) - Its a new version of FatCisBot Core, but with more stable code and new features!", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=350):
    """Clears a specified number of messages from the channel."""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} Messaged has been deleted from the channel!')

@bot.command(name='mute')
async def mute(ctx, member: discord.Member, *, reason=None):
    """Mutes a member by adding a mute role."""
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')  # get the mute role
    if not mute_role:
        # if the mute role does not exist, create it
        mute_role = await ctx.guild.create_role(name='Muted', reason='Mute command')
        for channel in ctx.guild.channels:
            # deny send messages permissions for the muted role in all channels
            await channel.set_permissions(mute_role, send_messages=False)
    
    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f'{member.mention} has been muted.')

@bot.command(name='unmute')
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} now can talk!")

@bot.command(name='membercount')
async def membercount(ctx):
    """Displays the number of members in the server."""
    member_count = ctx.guild.member_count
    await ctx.send(f'There are currently {member_count} members in this server.')


# run the bot with the token from Discord Developer Portal
bot.run("#Your token here")
