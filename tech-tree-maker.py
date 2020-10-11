import discord, json, time, os
from discord.ext import commands
from discord import Embed, File

#enter your bot token here
TOKEN = 'NzM2MTcxMjAwOTM3NDU5NzEy.Xxq62w.MuygcFLO6AmIATW2OUOKdSY55as'

#opens data.json and stores all data in data variable
with open("data.json") as f:
    data = json.load(f)

#change embed colour from here, dont remove "0x" from the the front of Hex value
embedColour = 0x26ceff

#list of civilisations
civilisations = ["aztecs",
"berbers",
"britons",
"bulgarians",
"burmese",
"byzantines",
"celts",
"chinese",
"cumans",
"ethiopians",
"franks",
"goths",
"huns",
"incas",
"indians",
"italians",
"japanese",
"khmer",
"koreans",
"lithuanians",
"magyars",
"malay",
"malians",
"mayans",
"mongols",
"persians",
"portuguese",
"saracens",
"slavs",
"spanish",
"tatars",
"teutons",
"turks",
"vietnamese",
"vikings"]

#List of sequence/headings of tech tree
techTreeHeadingList = ["blacksmith", "other", "siege", "infantry", "cavalry", "archers"]

gotoCivIndexList = []

civBannerLinksList = []

civIndexLink = []


gotoEmbed = Embed(description = '[GOTO CIV INDEX]')


#posts a temp msg that is later updated as hyperlink to civ index
async def post_goto_civ_index(ctx): 
    
    sentGotoCivIndex = await ctx.send(embed = gotoEmbed)
    gotoCivIndexList.append(sentGotoCivIndex)

#updates the goto civ index placeholder to the appropriate link
async def update_goto_civ_index(ctx):

    editedGotoEmbed = Embed(description = f'[GOTO CIV INDEX]({civIndexLink[0]})')
    loadingMessage = await ctx.send("Updating GOTO CIV INDEX Links\n\n(0/35)")
    for key, placeholder in enumerate(gotoCivIndexList):
        await placeholder.edit(embed = editedGotoEmbed)
        status = f"Updating GOTO CIV INDEX Links\n\n({int(key)+1}/35)"
        await loadingMessage.edit(content = status)
    completedMessage = await ctx.send("Process Complete\n\nDeleting this message in 5 seconds.\n\nThank you for using Discord Tech Tree Maker!")
    await loadingMessage.delete(delay = None)
    await completedMessage.delete(delay = 5.0)

#posts the civ banner
async def post_civ_banner(ctx, civ):
    sent = await ctx.send(file = File("civ-banners/" + civ + ".png"))
    link = "https://discord.com/channels/" + str(sent.guild.id) + "/" + str(sent.channel.id) + "/" + str(sent.id)
    civBannerLinksList.append(link)

#post civ description as an embed
async def post_civ_description(ctx, civ):
    newEmbed = Embed(description = data[civ]['description'], colour = embedColour)
    newEmbed.set_thumbnail(url = data[civ]['thumbnail']['url'])
    await ctx.send(embed = newEmbed) 

#make the tech-tree
async def post_tech_tree(ctx, civ):
    for heading in techTreeHeadingList:
        await ctx.send(f"{data['techtree'][heading]}")
        await ctx.send(file = File('technologies/' + civ + "/" + heading + ".png"))

#send the civ index embed
async def post_civ_index_embed(ctx):

    civIndexBannerData = await ctx.send(file = File("civ-banners/_civilisations.png"))
    link = "https://discord.com/channels/" + str(civIndexBannerData.guild.id) + "/" + str(civIndexBannerData.channel.id) + "/" + str(civIndexBannerData.id)
    civIndexLink.append(link)

    myEmbed1 = ''
    myEmbed2 = ''
    myEmbed3 = ''
    
    for key, civ in enumerate(civilisations):
            if int(key) < 11: 
                myEmbed1 += f":small_blue_diamond:[" + civ.capitalize() + "](" + civBannerLinksList[key] + ") \n\n"
            if int(key) >= 11 and key < 23:
                myEmbed2 += f":small_blue_diamond:[" + civ.capitalize() + "](" + civBannerLinksList[key] + ") \n\n"
            if int(key) >=23:
                myEmbed3 += f":small_blue_diamond:[" + civ.capitalize() + "](" + civBannerLinksList[key] + ") \n\n"
        
    myCivIndexEmbed1 = Embed(description = myEmbed1, colour = embedColour)
    myCivIndexEmbed2 = Embed(description = myEmbed2, colour = embedColour)
    myCivIndexEmbed3 = Embed(description = myEmbed3, colour = embedColour)
    myCivIndexEmbed3.set_footer(text = data['footer']['content'])

    await ctx.send(embed = myCivIndexEmbed1)
    await ctx.send(embed = myCivIndexEmbed2)
    await ctx.send(embed = myCivIndexEmbed3)


client = commands.Bot(command_prefix = '!')

@client.command(name = 'hello')
async def send_image(ctx):
    #await ctx.send('hi')
    
    #to send a file
    await ctx.send(file = File("test.png"))

@client.command(name = 'start')
async def send_embed(ctx):
    for civ in civilisations:
        await post_goto_civ_index(ctx)
        await post_civ_banner(ctx, civ)
        await post_civ_description(ctx, civ)
        await post_tech_tree(ctx, civ)
        time.sleep(0.5)
    await post_civ_index_embed(ctx)
    await update_goto_civ_index(ctx)


@client.event
async def on_ready():
    print('BOT IS READY!')
    print(f'Your CWD is: {os.getcwd()}')

client.run(TOKEN)

