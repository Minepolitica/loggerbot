import configparser
import discord
from discord.ext import commands

config = configparser.ConfigParser()
config.read("credentials.cfg")

bot_token = config.get("default", "bot_token")
log_channel_id = config.get("default", "log_channel_id")

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.voice_states = True
intents.guilds = True
intents.invites = True
intents.members = True
intents.guild_reactions = True


bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
# Printing when bot properly starts
async def on_ready():
    print(f'Logged in as {bot.user.name} bot')

# Logging the embed into the log channel
async def log_to_channel(embed):
    channel = bot.get_channel(log_channel_id)
    if channel is not None:
        await channel.send(embed=embed)
    else:
        print("Log channel not found.")

# Creating the embed
def create_embed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Logged by your bot")
    return embed



@bot.event
# When user joins create guild and nickname values
async def on_member_join(member):
    guild = member.guild
    nickname = member.display_name

    # Creating the embed with action info
    embed = create_embed(
        title="Member Joined",
        description=(
            f"**Date:** {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Server:** {guild.name} (ID: {guild.id})\n\n"
            f"**User:** {member} (ID: {member.id})\n\n"
            f"**Nickname:** {nickname}\n"
        ),
        color=discord.Color.green()  # Green for user joining the server
    )
    
    # Loging the embed into the log channel
    await log_to_channel(embed)



@bot.event
async def on_member_remove(member):
    guild = member.guild
    nickname = member.display_name

    embed = create_embed(
        title="Member Left",
        description=(
            f"**Date:** {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Server:** {guild.name} (ID: {guild.id})\n\n"
            f"**User:** {member} (ID: {member.id})\n\n"
            f"**Nickname:** {nickname}\n"
        ),
        color=discord.Color.red()  # Red for user leaving the server
    )
    
    await log_to_channel(embed)



@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return

    guild = after.guild
    nickname = before.author.display_name

    embed = create_embed(
        title="Message Edited",
        description=(
            f"**Date:** {after.edited_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Server:** {guild.name} (ID: {guild.id})\n\n"
            f"**Channel:** {after.channel.name} (ID: {after.channel.id})\n\n"
            f"**User:** {before.author} (ID: {before.author.id})\n\n"
            f"**Nickname:** {nickname}\n\n"
            f"**Message ID:** {before.id}\n\n"
            f"**Before Edit:** {before.content}\n\n"
            f"**After Edit:** {after.content}\n"
            "test 2 bruh"
        ),
        color=discord.Color.orange()  # Orange for message edited
    )
    
    await log_to_channel(embed)



@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return

    guild = message.guild
    nickname = message.author.display_name

    embed = create_embed(
        title="Message Deleted",
        description=(
            f"**Date:** {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Server:** {guild.name} (ID: {guild.id})\n\n"
            f"**Channel:** {message.channel.name} (ID: {message.channel.id})\n\n"
            f"**User:** {message.author} (ID: {message.author.id})\n\n"
            f"**Nickname:** {nickname}\n\n"
            f"**Message ID:** {message.id}\n\n"
            f"**Message:** {message.content}\n"
        ),
        color=discord.Color.red()  # Light red for message deleted
    )
    
    await log_to_channel(embed)



@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        guild = member.guild
        nickname = member.display_name

        if before.channel is None:
            embed = create_embed(
                title="User Joined Voice Channel",
                description=(
                    f"**Date:** {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"**Server:** {guild.name} (ID: {guild.id})\n\n"
                    f"**Channel:** {after.channel.name} (ID: {after.channel.id})\n\n"
                    f"**User:** {member} (ID: {member.id})\n\n"
                    f"**Nickname:** {nickname}\n"
                ),
                color=discord.Color.from_rgb(144, 238, 144)  # Very light green for voice channel join
            )
        elif after.channel is None:
            embed = create_embed(
                title="User Left Voice Channel",
                description=(
                    f"**Date:** {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"**Server:** {guild.name} (ID: {guild.id})\n\n"
                    f"**Channel:** {before.channel.name} (ID: {before.channel.id})\n\n"
                    f"**User:** {member} (ID: {member.id})\n\n"
                    f"**Nickname:** {nickname}\n"
                ),
                color=discord.Color.from_rgb(255, 182, 193)  # Very light red for voice channel leave
            )
        else:
            return

        await log_to_channel(embed)

@bot.event
async def on_invite_create(invite):
    guild = invite.guild
    inviter = invite.inviter

    embed = create_embed(
        title = "Invite Link Has Been Created",
        description=(
            f"**Date:** {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Server:** {guild.name} (ID: {guild.id})\n\n"
            f"**Channel:** {invite.channel.name} (ID: {invite.channel.id})\n\n"
            f"**Inviter:** {inviter} (ID: {inviter.id})\n\n"
            f"**Invite Code:** {invite.code}\n\n"
            f"**Max Uses:** {invite.max_uses}\n\n"
            f"**Expires At:** {invite.expires_at}\n"
        ),
        color=discord.Color.from_rgb(0, 191, 255) # Light blue for invite creation
    )

    await log_to_channel(embed)

@bot.event
async def channel_update(ch_update):
    pass

bot.run(bot_token)
