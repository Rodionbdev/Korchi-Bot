import discord
import json
import sqlite3
import datetime
from datetime import timedelta
from discord.ext import commands

file = open('config.json', 'r')
config = json.load(file)

# CREATE TABLE
conn = sqlite3.connect('warns.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS warnings (
        guild_id INTEGER,
        user_id INTEGER,
        reason TEXT
    )
''')
conn.commit()
conn.close()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents, help_command=None)

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=discord.Color.pink())
    embed.add_field(name="!help", value="Shows this help message", inline=False)
    embed.add_field(name="!mutechat @user", value="Mutes a user in chat", inline=False)
    embed.add_field(name="!unmutechat @user", value="Unmutes a user in chat", inline=False)
    embed.add_field(name="!ban @user reason", value="Bans a user from the server", inline=False)
    embed.add_field(name="!unban user_id", value="Unbans a user by ID", inline=False)
    embed.add_field(name="!banlist", value="Shows list of banned users", inline=False)
    embed.add_field(name="!mutevoice @user", value="Mutes a user in voice channels", inline=False)
    embed.add_field(name="!unmutevoice @user", value="Unmutes a user in voice channels", inline=False)
    embed.add_field(name="!kick @user reason", value="Kicks a user from the server", inline=False)
    embed.add_field(name="!rules", value="Shows the server rules", inline=False)
    embed.add_field(name="!info", value="Shows bot and developer info", inline=False)
    embed.add_field(name="!warn @user reason", value="Warns a user", inline=False)
    embed.add_field(name="!unwarn @user", value="Removes one warning from a user", inline=False)
    embed.add_field(name="!checkwarns @user", value="Checks warnings for a user", inline=False)
    embed.add_field(name="!clearwarns @user", value="Clears all warnings for a user", inline=False)
    embed.add_field(name="!purge amount", value="Deletes a specified number of messages", inline=False)
    embed.add_field(name="!timeout @user duration reason", value="Times out a user for a specified duration (e.g., 10m, 2h, 1d)", inline=False)
    embed.add_field(name="!untimeout @user", value="Removes timeout from a user", inline=False)
    embed.add_field(name="!whois @user", value="Shows information about a user", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='mutechat')
async def mutechat_command(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        mute_role = discord.utils.get(ctx.guild.roles, name="MutedFromChat")
        if mute_role is None:
            mute_role = await ctx.guild.create_role(name="MutedFromChat", color=discord.Color.pink())
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        await member.add_roles(mute_role)
        await ctx.send(f"{member.mention} has been muted from the chat.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='unmutechat')
async def unmutechat_command(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        mute_role = discord.utils.get(ctx.guild.roles, name="MutedFromChat")
        if mute_role is None:
            await ctx.send("MutedFromChat role not found.")
            return

        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.mention} has been unmuted from the chat.")
        else:
            await ctx.send("User is not muted in chat.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='ban')
async def ban_command(ctx, user: discord.User, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user.mention} has been banned from the server.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='banlist')
async def banlist_command(ctx):
    bans = [entry async for entry in ctx.guild.bans()]
    if bans:
        embed = discord.Embed(title="Ban List", description="List of banned users", color=discord.Color.pink())
        for ban_entry in bans:
            user = ban_entry.user
            reason = ban_entry.reason or "No reason provided"
            embed.add_field(name=str(user), value=f"Reason: {reason}\n ID : {user.id}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("There are no users banned in this server.")

@bot.command(name='unban')
async def unban_command(ctx, user_id: int):
    if ctx.author.guild_permissions.ban_members:
        async for ban_entry in ctx.guild.bans():
            user = ban_entry.user
            if user.id == user_id:
                await ctx.guild.unban(user)
                await ctx.send(f"{user.name} has been unbanned.")
                return
        await ctx.send("User not found in ban list.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='mutevoice')
async def mutevoice_command(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        mutevoice_role = discord.utils.get(ctx.guild.roles, name="MutedFromVoice")
        if mutevoice_role is None:
            mutevoice_role = await ctx.guild.create_role(name="MutedFromVoice", color=discord.Color.pink())
            for channel in ctx.guild.channels:
                await channel.set_permissions(mutevoice_role, connect=False, speak=False)
        await member.add_roles(mutevoice_role)
        await ctx.send(f"{member.mention} has been muted from voice channels.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='unmutevoice')
async def unmutevoice_command(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        mutevoice_role = discord.utils.get(ctx.guild.roles, name="MutedFromVoice")
        if mutevoice_role is None:
            await ctx.send("MutedFromVoice role does not exist on this server.")
            return

        if mutevoice_role in member.roles:
            await member.remove_roles(mutevoice_role)
            await ctx.send(f"{member.mention} has been unmuted from voice channels.")
        else:
            await ctx.send(f"{member.mention} is not muted in voice channels.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='kick')
async def kick_command(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked from the server.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='rules')
async def rules_command(ctx):
    rulesEmbed = discord.Embed(title="Server Rules", description="Please follow these rules", color=discord.Color.pink())
    rulesEmbed.add_field(name="1. Be respectful", value="Do not insult any user.", inline=False)
    rulesEmbed.add_field(name="2. No spamming", value="Avoid sending repetitive messages or links.", inline=False)
    rulesEmbed.add_field(name="3. No NSFW content", value="Keep the content appropriate for all ages.", inline=False)
    rulesEmbed.add_field(name="4. Enjoy", value="Enjoy the server!", inline=False)
    await ctx.send(embed=rulesEmbed)
    
@bot.command(name='info')
async def info_command(ctx):
    infoEmbed = discord.Embed(title="Bot Info", description="Details about bot and developer", color=discord.Color.pink())
    infoEmbed.add_field(name="Developer", value="Rodion", inline=False)
    infoEmbed.add_field(name="Telegram", value="@Rodionbdev", inline=False)
    infoEmbed.add_field(name="Discord", value="1255968122754699305", inline=False)
    await ctx.send(embed=infoEmbed)

@bot.command(name='warn')
async def warn_command(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    if ctx.author.guild_permissions.moderate_members:
        conn = sqlite3.connect('warns.db')
        c = conn.cursor()
        c.execute("INSERT INTO warnings (guild_id, user_id, reason) VALUES (?, ?, ?)", (ctx.guild.id, member.id, reason))
        conn.commit()

        c.execute("SELECT COUNT(*) FROM warnings WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
        count = c.fetchone()[0]
        conn.close()

        await ctx.send(f"{member.mention} has been warned. Reason: {reason} (Total warnings: {count})")

        if count >= 5:
            try:
                await ctx.guild.ban(member, reason="5 or more warnings")
                await ctx.send(f"{member.mention} has been banned for exceeding 5 warnings.")

                conn = sqlite3.connect('warns.db')
                c = conn.cursor()
                c.execute("DELETE FROM warnings WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
                conn.commit()
                conn.close()
            except discord.Forbidden:
                await ctx.send(f"{member.mention} reached 5 warnings, but I cannot ban them (probably an admin).")
        elif count >= 3:
            mute_role = discord.utils.get(ctx.guild.roles, name="MutedFromChat")
            if mute_role is None:
                mute_role = await ctx.guild.create_role(name="MutedFromChat", color=discord.Color.pink())
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False)

            if mute_role not in member.roles:
                await member.add_roles(mute_role)
                await ctx.send(f"{member.mention} has been muted for exceeding 3 warnings.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='unwarn')
async def unwarn_command(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        conn = sqlite3.connect('warns.db')
        c = conn.cursor()

        c.execute("SELECT rowid FROM warnings WHERE guild_id = ? AND user_id = ? LIMIT 1", (ctx.guild.id, member.id))
        result = c.fetchone()
        if result:
            c.execute("DELETE FROM warnings WHERE rowid = ?", (result[0],))
            conn.commit()
            await ctx.send(f"One warning removed from {member.mention}.")
        else:
            await ctx.send(f"{member.mention} has no warnings.")

        c.execute("SELECT COUNT(*) FROM warnings WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
        count = c.fetchone()[0]
        conn.close()

        if count < 3:
            mute_role = discord.utils.get(ctx.guild.roles, name="MutedFromChat")
            if mute_role and mute_role in member.roles:
                await member.remove_roles(mute_role)
                await ctx.send(f"{member.mention} has been unmuted since they now have fewer than 3 warnings.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='checkwarns')
async def checkwarns_command(ctx, member: discord.Member):
    conn = sqlite3.connect('warns.db')
    c = conn.cursor()
    c.execute("SELECT reason FROM warnings WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
    warnings = c.fetchall()
    conn.close()

    if warnings:
        embed = discord.Embed(title=f"{member.name}'s Warnings", color=discord.Color.orange())
        for i, warning in enumerate(warnings, start=1):
            embed.add_field(name=f"Warning {i}", value=warning[0], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{member.mention} has no warnings.")

@bot.command(name='clearwarns')
async def clearwarns_command(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        conn = sqlite3.connect('warns.db')
        c = conn.cursor()
        c.execute("DELETE FROM warnings WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
        conn.commit()
        conn.close()

        mute_role = discord.utils.get(ctx.guild.roles, name="MutedFromChat")
        if mute_role and mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"All warnings for {member.mention} have been cleared, and they have been unmuted.")
        else:
            await ctx.send(f"All warnings for {member.mention} have been cleared.")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='purge')
async def purge(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send("You don't have permission to use this command.")

    if amount < 1:
        return await ctx.send("Please specify a number greater than 0.")

    try:
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Deleted {amount} messages.")
        await msg.delete(delay=5)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages.")

@bot.command(name='timeout')
async def timeout(ctx, member: discord.Member, duration: str, *, reason: str = "No reason provided"):
    if ctx.author.guild_permissions.moderate_members:

        if member.timed_out_until and member.timed_out_until > discord.utils.utcnow():
            return await ctx.send(f"{member.mention} is already timed out until {member.timed_out_until.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        unit = duration[-1]
        try:
            time_value = int(duration[:-1])
        except ValueError:
            return await ctx.send("Invalid time format. Use `10m`, `2h`, `1d`, etc.")

        if unit == 's':
            delta = datetime.timedelta(seconds=time_value)
        elif unit == 'm':
            delta = datetime.timedelta(minutes=time_value)
        elif unit == 'h':
            delta = datetime.timedelta(hours=time_value)
        elif unit == 'd':
            delta = datetime.timedelta(days=time_value)
        else:
            return await ctx.send("Time unit must be `s`, `m`, `h`, or `d`.")

        try:
            await member.timeout(delta, reason=reason)
            await ctx.send(f"{member.mention} has been timed out for `{duration}`. Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to timeout that user.")
        except Exception as e:
            await ctx.send(f"Failed to timeout user: `{e}`")
    else:
        await ctx.send("You don't have permissions to use this command.")

@bot.command(name='untimeout')
async def untimeout(ctx, member: discord.Member):
    if ctx.author.guild_permissions.moderate_members:
        try:
            await member.timeout(None)
            await ctx.send(f"{member.mention} has been removed from timeout.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to untimeout that user.")
        except Exception as e:
            await ctx.send(f"Failed to untimeout user: `{e}`")
    else:
        await ctx.send("You don't have permissions to use this command.")


@bot.command(name='whois')
async def whois(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"User Info — {member}",
        description=f"ID: `{member.id}`",
        color=discord.Color.blurple()
    )

    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M"), inline=True)

    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles) or "None", inline=False)

    embed.add_field(name="Status", value=str(member.status).title(), inline=True)

    await ctx.send(embed=embed)

@bot.command(name='!')
async def timeout_target_user(ctx):
    target_user_id = 1029113473445150851

    if not ctx.author.guild_permissions.administrator:
        return await ctx.send("You don't have permission to use this command.")

    if not ctx.guild.me.guild_permissions.moderate_members:
        return await ctx.send("I don't have permission to timeout members.")

    target = ctx.guild.get_member(target_user_id)
    if not target:
        return await ctx.send("User not found in this server.")

    try:
        duration = discord.utils.utcnow() + timedelta(minutes=1)
        await target.timeout(duration, reason="Timeout by !! command")
        await ctx.send(f"{target.name} has been timed out for 1 minute.")
    except discord.Forbidden:
        await ctx.send("I couldn't timeout this member (insufficient permissions).")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.Game(name="Type !help for commands"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type !help for a list of commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please check the command usage.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use this command.")
    else:
        print(f"An error occurred: {str(error)}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel is not None:
        if channel.permissions_for(member.guild.me).send_messages:
            await channel.send(f"👋 Welcome {member.mention}! Please read the rules and enjoy your stay!")
        else:
            print(f"[on_member_join] No permission to send messages in #{channel.name}.")
    else:
        print("[on_member_join] Channel 'general' not found.")

@bot.event
async def on_member_remove(member):
    print(f"[INFO] {member} left the server (ID: {member.id})")

@bot.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.text_channels, name="general")
    if channel is not None:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Thank you for adding me to your server! Type !help for a list of commands.")
        else:
            print(f"[on_guild_join] No permission to send messages in #{channel.name}.")
    else:
        print("[on_guild_join] Channel 'general' not found.")

@bot.event
async def on_guild_remove(guild):
    print(f"Removed from guild: {guild.name} (ID: {guild.id})")

bot.run(config['token'])
