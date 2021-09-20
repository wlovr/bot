import discord
import asyncio
import requests
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup

client = discord.Client()
개발자 = '사용자ㅣ! 용트름#3507'

webhook_file = '데이터/웹훅.txt'
message_file = '데이터/내용.txt'
title_file = '데이터/제목.txt'
image_file = '데이터/사진.txt'


@client.event
async def on_error(event, *args, **kwargs):
    pass


@client.event
async def banner_task():
    while True:
        message = open(message_file, 'r')
        message = message.read()

        title = open(title_file, 'r')
        title = title.read()

        image = open(image_file, 'r')
        image = image.read()

        x = []
        with open(webhook_file) as file:
            for l in file:
                response = requests.get(l.strip())
                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    if response.status_code == '{"message": "Unknown Webhook", "code": 10015}':
                        pass
                    else:
                        x.append(l.strip())

        webhook = DiscordWebhook(url=x)
        embed = DiscordEmbed(title=title, description=message, color=0xE84444)
        embed.set_image(url=image)
        embed.set_footer(text=개발자)
        webhook.set_content('@everyone')
        webhook.add_embed(embed)
        response = webhook.execute()

        with open(webhook_file, 'w') as filehandle:
            for listitem in x:
                filehandle.write('%s\n' % listitem)
        x.clear()

        await asyncio.sleep(3600)


@client.event
async def on_connect():
    print('[ - ] 봇 로그인 완료.')


@client.event
async def on_message(message):
    if message.content.startswith('트름아 추가'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            msg = message.content[7:]
            if msg == '':
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"웹훅을 입력 하여 주세요.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                return
            else:
                try:
                    response = requests.get(msg)
                except requests.exceptions.MissingSchema:
                    role = message.guild.me.top_role
                    embed = discord.Embed(description=f"추가 대상이 웹훅이 아닙니다.",
                                          colour=role.color)
                    embed.set_footer(text=개발자)
                    await message.channel.send(embed=embed)
                    return
                except requests.exceptions.InvalidURL:
                    role = message.guild.me.top_role
                    embed = discord.Embed(description=f"추가 대상이 웹훅이 아닙니다.",
                                          colour=role.color)
                    embed.set_footer(text=개발자)
                    await message.channel.send(embed=embed)
                    return

                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    if response.status_code == '{"message": "Unknown Webhook", "code": 10015}':
                        role = message.guild.me.top_role
                        embed = discord.Embed(description=f"유효 하지 않는 웹훅 입니다.",
                                              colour=role.color)
                        embed.set_footer(text=개발자)
                        await message.channel.send(embed=embed)
                    else:
                        if 'https://' in msg:
                            text = open(webhook_file, 'a')
                            text.write(msg)
                            text.write('\n')
                            role = message.guild.me.top_role
                            embed = discord.Embed(
                                description=f"웹훅을 성공적으로 추가 하였습니다.",
                                colour=role.color)
                            embed.set_footer(text=개발자)
                            await message.channel.send(embed=embed)
                            text.close()
                        else:
                            return

    if message.content.startswith('트름아 내용'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            msg = message.content[7:]
            if msg == '':
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"내용을 입력 하여 주세요.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                return
            else:
                text = open(message_file, 'w', -1, 'utf-8')
                text.write(msg)
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"내용 변경 하였습니다.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                text.close()
                return

    if message.content.startswith('트름아 제목'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            msg = message.content[7:]
            if msg == '':
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"제목을 입력 하여 주세요.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                return
            else:
                text = open(title_file, 'w', -1, 'utf-8')
                text.write(msg)
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"제목을 변경 하였습니다.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                text.close()
                return

    if message.content.startswith('트름아 사진'):
        if message.author.guild_permissions.manage_messages:
            await message.delete()
            msg = message.content[7:]
            if msg == '삭제':
                text = open(image_file, 'w')
                text.write('')
                text.close()
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"사진을 삭제 하였습니다.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                return

            if msg == '':
                role = message.guild.me.top_role
                embed = discord.Embed(description=f"사진을 입력 하여 주세요.",
                                      colour=role.color)
                embed.set_footer(text=개발자)
                await message.channel.send(embed=embed)
                return
            else:
                try:
                    u = (message.attachments[0].url)
                except:
                    u = ''

                if u == '':
                    u = msg
                    if 'https://' in msg:
                        text = open(image_file, 'w')
                        text.write(u)
                        role = message.guild.me.top_role
                        embed = discord.Embed(description=f"사진을 변경 하였습니다.",
                                              colour=role.color)
                        embed.set_footer(text=개발자)
                        await message.channel.send(embed=embed)
                        text.close()
                        return
                    else:
                        role = message.guild.me.top_role
                        embed = discord.Embed(description=f"사진을 입력 하여 주세요.",
                                              colour=role.color)
                        embed.set_footer(text=개발자)
                        await message.channel.send(embed=embed)
                        return
                else:
                    text = open(image_file, 'w')
                    text.write(u)
                    role = message.guild.me.top_role
                    embed = discord.Embed(description=f"내용 변경 하였습니다.",
                                          colour=role.color)
                    embed.set_footer(text=개발자)
                    await message.channel.send(embed=embed)
                    text.close()
                    return


client.loop.create_task(banner_task())
client.run('ODg5NTExOTM2MTMwMTU4NjYy.YUiUiw.Xs553XgN3jJEvDA_ICX8F51tUBY')
