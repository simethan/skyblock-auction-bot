import discord
import cmath
from discord.ext import commands
from discord import Permissions
from discord.utils import get
import asyncio
import json
import locale
import time
import requests
from requests import get
from json import loads, dump
import datetime
from json.decoder import JSONDecodeError
locale.setlocale(locale.LC_ALL, 'en_US')

def seconds_to_hms(seconds):
    out = []
    for ct in range(3)[::-1]:
        a, b = divmod(seconds, 60 ** ct)
        out.append(a)
        seconds = b
    return out

def remove1(a):
	counter_Alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	for n in range(0,10):
		counter = n 
		remove = "§" + str(counter)
		remove_1 = "§" + counter_Alpha[n]
		try:
			a = a.replace(remove,"")
			a = a.replace(remove_1,"")
			a = a.replace("§l","")
			a = a.replace("§o","")
			a = a.replace("§ka","")
			a = a.replace("§r","")
		except AttributeError:
			continue
	return(a)

token= 'UR-BOT-TOKEN-HERE'  ### TOKEN IDENTIFIER ###
APIKEY = 'UR-API-KEY-HERE'
client = commands.Bot(command_prefix = '/')
client.remove_command("help")
game = discord.Game("with- do /help")

@client.event  
async def on_ready():  
    print(f'We have logged in as {client.user}')  
    print()
    print("Discord.py Version " + discord.__version__)
    print()
    await client.change_presence(activity = game)  

@client.event
async def on_message(message):
    print()
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

@client.command()
async def s(ctx,*,un):
    await ctx.send(f"https://sky.shiiyu.moe/stats/{un}")
    await ctx.message.delete()

@client.command()
async def help(ctx,*,phrase = None):
    await ctx.send(f"<@!{ctx.message.author.id}>! ```/ac [ign] -- check active auctions \n/acl [ign] -- check active auctions with lore (use this if its a book!) \n/lb [item_name] -- (*note*: if item is a pet, rarity: 0 - common, 1 - uncommon, 2 - rare, 3 - epic, 4 - legendary. And for books, eg, Power 7 == power;7) \n/bz [item_name] -- for bazaar buy & sell prices! \n \nFor basic math commands: \n/add [num1] [num2] -- to add 2 numbers together.\n/sub [num1] [num2] -- to subtract one number from the other. \n/mtp [num1] [num2] -- to multiply both numbers.```")
    await ctx.message.delete()

@client.command()
async def p(ctx,*,p):
    await ctx.send(f"https://plancke.io/hypixel/guild/name/{p}")
    await ctx.message.delete()

@client.command()
async def purge(ctx,*,num):
       await ctx.message.delete()
       q = await ctx.channel.purge(limit=int(num))
       await ctx.send(':otter: '+f'Deleted {len(q)} message(s).')

"""SLOW METHOD OF GETTING PLAYER AUCTIONS WITHOUT LORE"""

@client.command()
async def ac_slow(ctx,*,un):
    pp = await ctx.send(f"<@!{ctx.message.author.id}>! Finding auctions for {un}..")
    await ctx.message.delete()
    uuid_raw = requests.get("https://api.mojang.com/users/profiles/minecraft/"+un)
    uuid_json = json.loads(uuid_raw.text)
    uuid_json == uuid_raw.json
    uuid = uuid_json["id"]
    auction_pagesRaw = requests.get("https://api.hypixel.net/skyblock/auctions?key=API%20Key&page=0")
    auction_pagesJson = json.loads(auction_pagesRaw.text)
    auction_pagesJson == auction_pagesRaw.json
    pages  = auction_pagesJson["totalPages"]
    user_Auctions = []
    count = 1

    for n in range(pages+1):
        auction_raw = requests.get("https://api.hypixel.net/skyblock/auctions?key=API%20Key&page="+str(n))
        auction_json = json.loads(auction_raw.text)
        auction_json == auction_raw.json

        for i in range(len(auction_json["auctions"])):

            try:

                if auction_json["auctions"][i]["auctioneer"] == str(uuid):

                    if auction_json["auctions"][i]["claimed"] == False:
                        data = {"NAME":auction_json["auctions"][i]["item_name"],"BID":auction_json["auctions"][i]["highest_bid_amount"],"PRICE":auction_json["auctions"][i]["starting_bid"],"NUMBER":len(auction_json["auctions"][i]["bids"]),"TIER":auction_json["auctions"][i]["tier"],"AID":auction_json["auctions"][i]["uuid"],"TIME":auction_json["auctions"][i]["end"]}
                        user_Auctions.append(data)

            except KeyError:

                continue
    if len(user_Auctions) != 0:

        await pp.edit(content = f"<@!{ctx.message.author.id}>! Auctions found for {un}")

        for j in range(len(user_Auctions)):
            aid = user_Auctions[j]["AID"]
            a1 = aid[:8]
            a2 = aid[8:12]
            a3 = aid[12:16]
            a4 = aid[16:20]
            a5 = aid[20:-1]
            a6 = aid[-1]
            b = "/viewauction "+a1+"-"+a2+"-"+a3+"-"+a4+"-"+a5+a6
		
            time = int(user_Auctions[j]["TIME"])
            _end = datetime.datetime.fromtimestamp(time/1000)
            __end = (_end - datetime.datetime.now())
            end = ":".join([str(i).zfill(2) for i in ([__end.days] + seconds_to_hms(__end.seconds))])
		
            name = user_Auctions[j]["NAME"]
            price = user_Auctions[j]["PRICE"]
            price = locale.format("%d",int(price), grouping=True)
            bid = user_Auctions[j]["BID"]
            bid = locale.format("%d",int(bid), grouping=True)
            num = user_Auctions[j]["NUMBER"]
            tier = user_Auctions[j]["TIER"]

            if datetime.datetime.now() > _end:
                end = "AUCTION HAS ENDED"

            if user_Auctions[j]["NUMBER"] == 0:
                bid = "No Bidders!"
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for {un}!", color=0xFFF8E7)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Bids: ", value=bid, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                await ctx.send(embed=embedVar)

            if user_Auctions[j]["NUMBER"] != 0:
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for {un}!", color=0xFFF8E7)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Highest Bid: ", value=bid, inline=True)
                embedVar.add_field(name="Bidders: ", value=num, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                await ctx.send(embed=embedVar)

    elif len(user_Auctions) == 0 and count == 1:
        await pp.edit(content=f"<@!{ctx.message.author.id}>! No Auctions detected for {un}")

"""SLOW METHOD OF GETTING PLAYER AUCTION WITH LORE"""	
	
@client.command()
async def acl_slow(ctx,*,username):

    qq = await ctx.send(f"<@!{ctx.message.author.id}>! Finding auctions for {username}..")
    await ctx.message.delete()
    uuid_raw = requests.get("https://api.mojang.com/users/profiles/minecraft/"+username)
    uuid_json = json.loads(uuid_raw.text)
    uuid_json == uuid_raw.json
    uuid = uuid_json["id"]
    auction_pagesRaw = requests.get("https://api.hypixel.net/skyblock/auctions?key=API%20Key&page=0")
    auction_pagesJson = json.loads(auction_pagesRaw.text)
    auction_pagesJson == auction_pagesRaw.json
    pages  = auction_pagesJson["totalPages"]
    user_Auctions = []
    count = 1

    for n in range(pages+1):
        auction_raw = requests.get("https://api.hypixel.net/skyblock/auctions?key=API%20Key&page="+str(n))
        auction_json = json.loads(auction_raw.text)
        auction_json == auction_raw.json

        for i in range(len(auction_json["auctions"])):
            try:
                if auction_json["auctions"][i]["auctioneer"] == str(uuid):
                    if auction_json["auctions"][i]["claimed"] == False:
                        data = {"NAME":auction_json["auctions"][i]["item_name"],"BID":auction_json["auctions"][i]["highest_bid_amount"],"PRICE":auction_json["auctions"][i]["starting_bid"],"NUMBER":len(auction_json["auctions"][i]["bids"]),"LORE":remove1(auction_json["auctions"][i]["item_lore"]),"TIER":auction_json["auctions"][i]["tier"],"AID":auction_json["auctions"][i]["uuid"],"TIME":auction_json["auctions"][i]["end"]}
                        user_Auctions.append(data)
            except KeyError:
                continue

    if len(user_Auctions) != 0:
        await qq.edit(content = f"<@!{ctx.message.author.id}>! Auctions found for {username}")
        for j in range(len(user_Auctions)):
            aid = user_Auctions[j]["AID"]
            a1 = aid[:8]
            a2 = aid[8:12]
            a3 = aid[12:16]
            a4 = aid[16:20]
            a5 = aid[20:-1]
            a6 = aid[-1]
            b = "/viewauction "+a1+"-"+a2+"-"+a3+"-"+a4+"-"+a5+a6
            time = int(user_Auctions[j]["TIME"])
            _end = datetime.datetime.fromtimestamp(time/1000)
            __end = (_end - datetime.datetime.now())
            end = ":".join([str(i).zfill(2) for i in ([__end.days] + seconds_to_hms(__end.seconds))])
            name = user_Auctions[j]["NAME"]
            price = user_Auctions[j]["PRICE"]
            price = locale.format("%d",int(price), grouping=True)
            bid = user_Auctions[j]["BID"]
            bid = locale.format("%d",int(bid), grouping=True)
            num = user_Auctions[j]["NUMBER"]
            lore = user_Auctions[j]["LORE"]
            tier = user_Auctions[j]["TIER"]

            if datetime.datetime.now() > _end: 
                end = "AUCTION HAS ENDED"

            if user_Auctions[j]["NUMBER"] == 0:
                bid = "No Bidders!"
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for {username}!", color=0xFFF8E7)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Item Lore: ", value=lore, inline=False)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Bids: ", value=bid, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                await ctx.send(embed=embedVar)

            if user_Auctions[j]["NUMBER"] != 0:
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for {username}!", color=0xFFF8E7)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Item Lore: ", value=lore, inline=False)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Highest Bid: ", value=bid, inline=True)
                embedVar.add_field(name="Bidders: ", value=num, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                await ctx.send(embed=embedVar)
    elif len(user_Auctions) == 0 and count == 1:
        await qq.edit(content = f"<@!{ctx.message.author.id}>! No Auctions detected for {username}")

"""LOWEST BIN FOR ITEMS. DO /help TO FIND OUT HOW OR JUST TRY /lb [item_name] or smt"""	
	
@client.command()
async def lb(ctx,*,item):
    qqq = await ctx.send(f"<@!{ctx.message.author.id}> Finding lowest bin for {item}")
    await ctx.message.delete()
    item1 = item.upper()
    item2 = item1.replace(" ","_")
    lb = get("https://moulberry.codes/lowestbin.json")
    lb = lb.json()
    avatar = ctx.message.author.avatar_url or ctx.message.author.default_avatar_url
    t = datetime.datetime.now()
    tt = t.strftime("%H:%M:%S")

    try:
        lb_item = lb[f"{item2}"]
        lb_item = locale.format("%d",int(lb_item), grouping=True)
        embedVar = discord.Embed(title="BIN BOT.", description="", color=0x66ff00)
        await qqq.edit(content=f"<@!{ctx.message.author.id}> Found Lowest BIN for {item}")
        embedVar.add_field(name=f"Lowest BIN for {item}: ", value=lb_item, inline=False)
        embedVar.set_footer(icon_url = avatar,text=f" Requested By: {ctx.message.author} | Today At: {tt}")
    
    except KeyError:
        await qqq.edit(content=f"<@!{ctx.message.author.id}> Couldn't Find Lowest BIN for {item}")
        await ctx.send(f"```Lowest BIN for {item} could not be found, \nDo Note: for pets, rarity: 0 - common, 1 - uncommon, 2 - rare, 3 - epic, 4 - legendary\n And for books, eg, Power 7 == power;7 \nSend the command in the format: /lb [item];[level]```")
    await ctx.send(embed=embedVar)


"""BAZAAR PRICE INFO, kinda unstable cos slothpixel"""

@client.command()
async def bz(ctx,*,item):
    initial_message = await ctx.send(f"<@!{ctx.message.author.id}> Finding Bazaar Info for {item}")
    await ctx.message.delete()
    itemI = item.upper()
    itemId = itemI.replace(" ","_")
    baz = get(f"https://api.slothpixel.me/api/skyblock/bazaar/{itemId}")
    baz = baz.json()
    avatar = ctx.message.author.avatar_url or ctx.message.author.default_avatar_url
    t = datetime.datetime.now()
    tt = t.strftime("%H:%M:%S")
    try:
        sell = int(baz["quick_status"]["sellPrice"])
        sell = locale.format("%d",sell, grouping=True)
        buy = int(baz["quick_status"]["buyPrice"])
        buy = locale.format("%d",buy, grouping=True)
        await initial_message.edit(content=f"<@!{ctx.message.author.id}> Found Bazaar Info for {item}")
        embedVar = discord.Embed(title="Bazaar Bot.", description=f"Bazaar Info for {item}!", color=0x66ff00)
        embedVar.add_field(name="Sell Price: ", value=sell, inline=True)
        embedVar.add_field(name="Buy Price: ", value=buy, inline=True)
        embedVar.set_footer(icon_url = avatar,text=f" Requested By: {ctx.message.author} | Today At: {tt}")
        await ctx.send(embed=embedVar)
    except KeyError:
        await initial_message.edit(content=f"<@!{ctx.message.author.id}> Couldn't Find Bazaar Info for {item}")

"""" MATH STUFF, CAN IGNORE IF YOU WANT """"
"""" 
@client.command()
async def mtp(ctx,*,num):
    q = num.split(" ")
    num1 = int(q[0])
    num2 = int(q[-1])
    numend = num1 * num2
    numend = locale.format("%d",numend, grouping=True)
    num1 = locale.format("%d",num1, grouping=True)
    num2 = locale.format("%d",num2, grouping=True)
    await ctx.send(f"{num1} x {num2} = {numend}")
@client.command()
async def add(ctx,*,num):
    q = num.split(" ")
    num1 = int(q[0])
    num2 = int(q[-1])
    numend = num1 + num2
    numend = locale.format("%d",numend, grouping=True)
    num1 = locale.format("%d",num1, grouping=True)
    num2 = locale.format("%d",num2, grouping=True)
    await ctx.send(f"{num1} + {num2} = {numend}")
@client.command()
async def sub(ctx,*,num):
    q = num.split(" ")
    num1 = int(q[0])
    num2 = int(q[-1])
    numend = num1 - num2
    numend = locale.format("%d",numend, grouping=True)
    num1 = locale.format("%d",num1, grouping=True)
    num2 = locale.format("%d",num2, grouping=True)
    await ctx.send(f"{num1} - {num2} = {numend}") """ 

""" --FOR AUCTIONS WITHOUT LORE--"""
"""NOTE THAT PICTURE OF ITEM MAY NOT NECESSARILY ALW SHOW UP"""

@client.command()
async def ac(ctx,*,un):
    pp = await ctx.send(f"<@!{ctx.message.author.id}>! Finding auctions for `{un}`..")
    await ctx.message.delete()
    uuid_raw = requests.get("https://api.mojang.com/users/profiles/minecraft/"+un)
    uuid_json = json.loads(uuid_raw.text)
    uuid_json == uuid_raw.json
    uuid = uuid_json["id"]
    user_Auctions = []
    count = 1
    auction_raw = requests.get(f"https://api.hypixel.net/skyblock/auction?key={APIKEY}&player={uuid}")
    auction_json = json.loads(auction_raw.text)
    auction_json == auction_raw.json

    for i in range(len(auction_json["auctions"])):
        try:
            if auction_json["auctions"][i]["claimed"] == False:
                time1 = int(auction_json["auctions"][i]["end"])
                _end = datetime.datetime.fromtimestamp(time1/1000)
                if datetime.datetime.now() < _end:
                    data = {"NAME":auction_json["auctions"][i]["item_name"],"BID":auction_json["auctions"][i]["highest_bid_amount"],"PRICE":auction_json["auctions"][i]["starting_bid"],"NUMBER":len(auction_json["auctions"][i]["bids"]),"TIER":auction_json["auctions"][i]["tier"],"AID":auction_json["auctions"][i]["uuid"],"TIME":auction_json["auctions"][i]["end"]}
                    user_Auctions.append(data)
        except KeyError:
            continue
    if len(user_Auctions) != 0:
        await pp.edit(content = f"<@!{ctx.message.author.id}>! Auctions found for `{un}`")
	
        for j in range(len(user_Auctions)):
		
            t = datetime.datetime.now()
            tt = t.strftime("%H:%M:%S")
		
            aid = user_Auctions[j]["AID"]
            a1 = aid[:8]
            a2 = aid[8:12]
            a3 = aid[12:16]
            a4 = aid[16:20]
            a5 = aid[20:-1]
            a6 = aid[-1]
            b = "/viewauction "+a1+"-"+a2+"-"+a3+"-"+a4+"-"+a5+a6
		
            time = int(user_Auctions[j]["TIME"])
            _end = datetime.datetime.fromtimestamp(time/1000)
            __end = (_end - datetime.datetime.now())
            end = ":".join([str(i).zfill(2) for i in ([__end.days] + seconds_to_hms(__end.seconds))])
		
            name = user_Auctions[j]["NAME"]
            image = name.upper()
            image = image.replace(" ","_")
            image1 = f"https://sky.shiiyu.moe/item/{image}"
		
            price = user_Auctions[j]["PRICE"]
            price = locale.format("%d",int(price), grouping=True)
		
            bid = user_Auctions[j]["BID"]
            bid = locale.format("%d",int(bid), grouping=True)
		
            num = user_Auctions[j]["NUMBER"]
	
            tier = user_Auctions[j]["TIER"]
		
            avatar = ctx.message.author.avatar_url or ctx.message.author.default_avatar_url
	
            if user_Auctions[j]["NUMBER"] == 0:
			
                bid = "No Bidders!"
		
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for `{un}`!", color=0x66ff00)
                embedVar.set_thumbnail(url=image1)
                embedVar.add_field(name="ITEM NAME: ", value= name , inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Bids: ", value=bid, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                embedVar.set_footer(icon_url = avatar,text=f" Requested By: {ctx.message.author} | Today At: {tt}")
                await ctx.send(embed=embedVar)
		
            if user_Auctions[j]["NUMBER"] != 0:
		
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for `{un}`!", color=0x66ff00)
                embedVar.set_thumbnail(url=image1)
                embedVar.add_field(name="ITEM NAME: ", value= name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Highest Bid: ", value=bid, inline=True)
                embedVar.add_field(name="Bidders: ", value=num, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                embedVar.set_footer(icon_url = avatar,text=f" Requested By: {ctx.message.author} | Today At: {tt}")
                await ctx.send(embed=embedVar)
		
    elif len(user_Auctions) == 0 and count == 1:
        await pp.edit(content=f"<@!{ctx.message.author.id}>! No Auctions detected for `{un}`")

""" --FOR AUCTIONS WITH LORE--"""
"""NOTE THAT PICTURE OF ITEM MAY NOT NECESSARILY ALW SHOW UP"""

@client.command()
async def acl(ctx,*,un):
    pp = await ctx.send(f"<@!{ctx.message.author.id}>! Finding auctions for `{un}`..")
    await ctx.message.delete()
    uuid_raw = requests.get("https://api.mojang.com/users/profiles/minecraft/"+un)
    uuid_json = json.loads(uuid_raw.text)
    uuid_json == uuid_raw.json
    uuid = uuid_json["id"]
    user_Auctions = []
    count = 1
    auction_raw = requests.get(f"https://api.hypixel.net/skyblock/auction?key={APIKEY}&player={uuid}")
    auction_json = json.loads(auction_raw.text)
    auction_json == auction_raw.json

    for i in range(len(auction_json["auctions"])):
        try:
            if auction_json["auctions"][i]["claimed"] == False:
                time1 = int(auction_json["auctions"][i]["end"])
                _end = datetime.datetime.fromtimestamp(time1/1000)
                if datetime.datetime.now() < _end:
                    data = {"NAME":auction_json["auctions"][i]["item_name"],"LORE":remove1(auction_json["auctions"][i]["item_lore"]),"BID":auction_json["auctions"][i]["highest_bid_amount"],"PRICE":auction_json["auctions"][i]["starting_bid"],"NUMBER":len(auction_json["auctions"][i]["bids"]),"TIER":auction_json["auctions"][i]["tier"],"AID":auction_json["auctions"][i]["uuid"],"TIME":auction_json["auctions"][i]["end"]}
                    user_Auctions.append(data)
        except KeyError:
            continue
	
    if len(user_Auctions) != 0:
        await pp.edit(content = f"<@!{ctx.message.author.id}>! Auctions found for `{un}`")
	
        for j in range(len(user_Auctions)):
		
            t = datetime.datetime.now()
            tt = t.strftime("%H:%M:%S")
		
            aid = user_Auctions[j]["AID"]
            a1 = aid[:8]
            a2 = aid[8:12]
            a3 = aid[12:16]
            a4 = aid[16:20]
            a5 = aid[20:-1]
            a6 = aid[-1]
            b = "/viewauction "+a1+"-"+a2+"-"+a3+"-"+a4+"-"+a5+a6
		
            time = int(user_Auctions[j]["TIME"])
            _end = datetime.datetime.fromtimestamp(time/1000)
            __end = (_end - datetime.datetime.now())
            end = ":".join([str(i).zfill(2) for i in ([__end.days] + seconds_to_hms(__end.seconds))])
		
            name = user_Auctions[j]["NAME"]
            image = name.upper()
            image = image.replace(" ","_")
            image1 = f"https://sky.shiiyu.moe/item/{image}"
		
            price = user_Auctions[j]["PRICE"]
            price = locale.format("%d",int(price), grouping=True)
		
            bid = user_Auctions[j]["BID"]
            bid = locale.format("%d",int(bid), grouping=True)
		
            num = user_Auctions[j]["NUMBER"]
	
            tier = user_Auctions[j]["TIER"]
		
            lore = user_Auctions[j]["LORE"]
	
            avatar = ctx.message.author.avatar_url or ctx.message.author.default_avatar_url
		
            if user_Auctions[j]["NUMBER"] == 0:
		
                bid = "No Bidders!"
		
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for `{un}`!", color=0x66ff00)
                embedVar.set_thumbnail(url=image1)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Item Lore: ", value=lore, inline=False)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Bids: ", value=bid, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                embedVar.set_footer(icon_url = avatar, text=f" Requested By: {ctx.message.author} | Today At: {tt}")
		
                await ctx.send(embed=embedVar)
		
            if user_Auctions[j]["NUMBER"] != 0:
		
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for `{un}`!", color=0x66ff00)
                embedVar.set_thumbnail(url=image1)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Item Lore: ", value=lore, inline=False)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Highest Bid: ", value=bid, inline=True)
                embedVar.add_field(name="Bidders: ", value=num, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
                embedVar.set_footer(icon_url = avatar, text=f" Requested By: {ctx.message.author} | Today At: {tt}")
		
                await ctx.send(embed=embedVar)
		
    elif len(user_Auctions) == 0 and count == 1:
        await pp.edit(content=f"<@!{ctx.message.author.id}>! No Auctions detected for `{un}`")
	
"""PROBS DOESNT WORK BUT U CAN TRY IDK"""	
"""NOTE THAT PICTURE OF ITEM MAY NOT NECESSARILY ALW SHOW UP"""

@client.command()
async def myah(ctx,*,phrase=None):
    un = ctx.message.author.display_name
    pp = await ctx.send(f"<@!{ctx.message.author.id}>! Finding auctions for `{un}`..")
    await ctx.message.delete()
    uuid_raw = requests.get("https://api.mojang.com/users/profiles/minecraft/"+un)
    uuid_json = json.loads(uuid_raw.text)
    uuid_json == uuid_raw.json
    uuid = uuid_json["id"]
    user_Auctions = []
    count = 1
    auction_raw = requests.get(f"https://api.hypixel.net/skyblock/auction?key={APIKEY}&player={uuid}")
    auction_json = json.loads(auction_raw.text)
    auction_json == auction_raw.json
	
    for i in range(len(auction_json["auctions"])):
        try:
		
            if auction_json["auctions"][i]["claimed"] == False:
		
                time1 = int(auction_json["auctions"][i]["end"])
                _end = datetime.datetime.fromtimestamp(time1/1000)
		
                if datetime.datetime.now() < _end:
			
                    data = {"NAME":auction_json["auctions"][i]["item_name"],"BID":auction_json["auctions"][i]["highest_bid_amount"],"PRICE":auction_json["auctions"][i]["starting_bid"],"NUMBER":len(auction_json["auctions"][i]["bids"]),"TIER":auction_json["auctions"][i]["tier"],"AID":auction_json["auctions"][i]["uuid"],"TIME":auction_json["auctions"][i]["end"]}
                    user_Auctions.append(data)
			
        except KeyError:
		
            continue
    if len(user_Auctions) != 0:
	
        await pp.edit(content = f"<@!{ctx.message.author.id}>! Auctions found for `{un}`")
	
        for j in range(len(user_Auctions)):
		
            aid = user_Auctions[j]["AID"]
            a1 = aid[:8]
            a2 = aid[8:12]
            a3 = aid[12:16]
            a4 = aid[16:20]
            a5 = aid[20:-1]
            a6 = aid[-1]
            b = "/viewauction "+a1+"-"+a2+"-"+a3+"-"+a4+"-"+a5+a6
		
            time = int(user_Auctions[j]["TIME"])
            _end = datetime.datetime.fromtimestamp(time/1000)
            __end = (_end - datetime.datetime.now())
            end = ":".join([str(i).zfill(2) for i in ([__end.days] + seconds_to_hms(__end.seconds))])
		
            name = user_Auctions[j]["NAME"]
	
            price = user_Auctions[j]["PRICE"]
            price = locale.format("%d",int(price), grouping=True)
	
            bid = user_Auctions[j]["BID"]
            bid = locale.format("%d",int(bid), grouping=True)
	
            num = user_Auctions[j]["NUMBER"]
		
            tier = user_Auctions[j]["TIER"]
	
            if user_Auctions[j]["NUMBER"] == 0:
			
                bid = "No Bidders!"
		
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for `{un}`!", color=0xFFF8E7)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Bids: ", value=bid, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
		
                await ctx.send(embed=embedVar)
		
            if user_Auctions[j]["NUMBER"] != 0:
		
                embedVar = discord.Embed(title="Auction Bot.", description=f"Auctions for `{un}`!", color=0xFFF8E7)
                embedVar.add_field(name="ITEM NAME: ", value=name, inline=True)
                embedVar.add_field(name="RARITY: ", value=tier, inline=True)
                embedVar.add_field(name="Starting Price: ", value=price, inline=True)
                embedVar.add_field(name="Highest Bid: ", value=bid, inline=True)
                embedVar.add_field(name="Bidders: ", value=num, inline=True)
                embedVar.add_field(name="Ends in: ", value=end, inline=True)
                embedVar.add_field(name="For this auction, do:", value=b, inline=True)
		
                await ctx.send(embed=embedVar)
		
    elif len(user_Auctions) == 0 and count == 1:
        await pp.edit(content=f"<@!{ctx.message.author.id}>! No Auctions detected for `{un}`")

client.run(token)

