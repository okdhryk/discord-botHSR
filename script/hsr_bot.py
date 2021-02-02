#!/usr/bin/env python
import argparse
import json
import os
import urllib.pasrse
import urllib.request

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

import discord
from discord.ext import commands

# define config value form config/config.json
with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.json') as j:
        config = json.load(j)

TOKEN_DISCORD = config['discord']['api_token']


prefix = '!'





client = discord.Client()

class Greet(commands.Cog, name='あいさつ'):
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @commands.command(name="こんにちは")
        async def hello(self, ctx):
        #出会いのあいさつをする
            await ctx.send(f"どうも、{ctx.author.name}さん!")

        @commands.command(name="さようなら")
        async def goodbye(self, ctx):
       #別れの挨拶をする"""
            await ctx.send(f"じゃあね、{ctx.author.name}さん!")
                                                                                    

class JapaneseHelpCommand(commands.DefaultHelpCommand):
        def __init__(self):
            super().__init__()
            self.commands_heading = "コマンド:"
            self.no_category = "その他"
            self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"

        def get_ending_note(self):
            return (f"各コマンドの説明: {prefix}help <コマンド名>\n"
                    f"各カテゴリの説明: {prefix}help <カテゴリ名>\n")

                                                                    





async def greet():
    channel = client.get_channel(804924906587816007)
    await channel.send('おはよう！')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await greet() # 挨拶する非同期関数を実行
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '/neko':
        await message.channel.send('にゃーん', file=discord.File('cat.jpg'))


def process_image(msg):
    try:
        bridge = CvBridge()
        orig = bridge.imgmsg_to_cv2(msg, "bgr8")
        img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        cv2.imshow('image', img)
        cv2.waitKey(1)
    except Exception as err:
        print( err)

def start_node():
    rospy.init_node('img_proc')
    rospy.loginfo('img_proc node started')
    rospy.Subscriber("image_raw", Image, process_image)
    rospy.spin()

if __name__ == '__main__':
    try:
        bot = commands.Bot(command_prefix=prefix, help_command=JapaneseHelpCommand())
        bot.add_cog(Greet(bot=bot))
        bot.run('ODA0OTE3NDQyMDQ0MTAwNjQ4.YBTTyA.H8EXQJVi9oJOqr3-iz4BUp1dDxc')

#        client.run('ODA0OTE3NDQyMDQ0MTAwNjQ4.YBTTyA.H8EXQJVi9oJOqr3-iz4BUp1dDxc')
    #    start_node()
    except rospy.ROSInterruptException:
        pass
    
