from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
load_dotenv()
from discord.ext import commands

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

SUPPORT_CATEGORY_NAME = "SUPPORT"  # 변경 가능

# 역할 이름 설정
ROLE_NAME = "장성급 장교 | general Officer"

# 봇이 준비되면 실행되는 이벤트 핸들러
@client.event
async def on_ready():
    print("봇이 로그인했습니다.")

# 킥 명령어
@client.command()
@commands.has_role(ROLE_NAME)
async def 킥(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "이유가 지정되지 않았습니다."
    await member.send(f"{member.name}님, {reason}")
    await member.kick(reason=reason)
    await ctx.send(f"{member}님이 킥되었습니다. 이유: {reason}")

# 밴 명령어
@client.command()
@commands.has_role(ROLE_NAME)
async def 밴(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = "이유가 지정되지 않았습니다."
    await member.send(f"{member.name}님, {reason}")
    await member.ban(reason=reason)
    await ctx.send(f"{member}님이 밴되었습니다. 이유: {reason}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!신청'):
        embed = discord.Embed(title='신청 종류', description='어떤 것을 신청하시겠습니까?', color=0xff0000)
        embed.add_field(name='1. 휴가', value='휴가를 신청합니다.')
        embed.add_field(name='2. 전역', value='전역을 신청합니다.')
        await message.channel.send(embed=embed)

    elif message.content.startswith('!휴가'):
        await message.channel.send('휴가 신청서를 작성하십시오. 이름을 입력해주세요.')

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('시간이 초과되었습니다.')
            return
        name = msg.content

        await message.channel.send('이유를 입력해주세요.')
        try:
            msg = await client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('시간이 초과되었습니다.')
            return
        reason = msg.content

        # 적은 내용을 특정 채널에 멘션하면서 전송
        output_channel = client.get_channel(1077175911729860628) # 적절한 채널 ID를 넣어주세요
        output_role = message.guild.get_role(1077041474505543811) # 적절한 역할 ID를 넣어주세요
        msg = await output_channel.send(f'{output_role.mention} {name}님께서 {reason} 이유로 휴가를 신청하셨습니다.')

        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

    elif message.content.startswith('!전역'):
        await message.channel.send('국군통수권자에게 문의하십시오.')

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        if str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌":
            channel = reaction.message.channel
            role = channel.guild.get_role(1077041474505543811) # 적절한 역할 ID를 넣어주세요
            if role in user.roles:
                if str(reaction.emoji) == "✅":
                    await channel.send(f'{reaction.message.author.mention} {user.mention}님이 휴가 신청을 승인하셨습니다.')
                else:
                    await channel.send(f'{reaction.message.author.mention} {user.mention}님이 휴가 신청을 미승인하셨습니다.')

       
try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
