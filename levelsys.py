import discord
from discord.ext import commands
from discord import User
from discord.ext.commands import Bot, guild_only
from pymongo import MongoClient


bot_channel = #buraya botun mesaj atıcagı channeliin idsi 
talk_channels = [#buraya botun mesajları aldığı kanallar ]

level = ["Pan","Nypmha","Dryades"] #buraya level atlayınca hangi rolleri vermesi fln 
levelnum = [5,10,15] #ne kadar varsa o kadar 5'in katlarıyla gidin.

cluster = MongoClient("mongodb+srv://<password>:username@cluster0.iqtmc.mongodb.net/<dbname>?retryWrites=true&w=majority") #buraya mongodb url'niz <password> yerındekı parantezleri cıkarn.

levelling = cluster["discord"]["levelling"]  #buraya clusterlarının isimlerini gir 

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("adaxsasdkaskag")

    @commands.Cog.listener()
    async def on_message(self, message):            #level
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp":100}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
                    lvl = 0 
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Bol silenoslanmalar {message.author.mention}! Level atladın **level: {lvl}**!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(description=f"{message.author.mention} Rol aldın role: **{level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):          #rank yeri 
        if ctx.channel.id == bot_channel:
            stats = levelling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(descrpition="Mesaj göndermemişsin.")
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*lvl)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                rankings = levelling.find().sort("xp",-1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="İsim", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name="Sıralama", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="İlerleme durumu[lvl]",value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=True)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)




    @commands.command()
    async def liderler(self, ctx):           #topları gösterir
        if (ctx.channel.id == bot_channel):
            rankings = levelling.find().sort("xp",-1)
            i = 1
            embed = discord.Embed(title="liderler:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                        break
            await ctx.channel.send(embed=embed)








def setup(client):
    client.add_cog(levelsys(client))
