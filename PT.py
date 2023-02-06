import discord
from discord import app_commands
from discord.ext import commands
import os
from papago import Translator

PAPAGO = Translator(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self):
       # This copies the global commands over to your guild.
        for guild in self.guilds:
            print("guild.id",guild.id)
            self.tree.copy_global_to(guild=discord.Object(id=guild.id))
            await self.tree.sync(guild=discord.Object(id=guild.id))

    
    async def on_ready(self):
        print('Login:',self.user)
        await self.setup_hook()

intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.tree.command()
@app_commands.describe(
    message='The message you want to translate'
)
@app_commands.choices(transfrom=[
        app_commands.Choice(name="Korean", value="ko"),
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="Japanese", value="ja"),
        app_commands.Choice(name="Chinese(Simplified)", value="zh-cn"),
        app_commands.Choice(name="Chinese(Traditional)", value="zh-tw"),
        app_commands.Choice(name="Spanish", value="es"),
        app_commands.Choice(name="French", value="fr"),
        app_commands.Choice(name="Vietnamese", value="vi"),
        app_commands.Choice(name="Thai", value="th"),
        app_commands.Choice(name="Indonesia", value="id"),
        ])
@app_commands.choices(transto=[
        app_commands.Choice(name="Korean", value="ko"),
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="Japanese", value="ja"),
        app_commands.Choice(name="Chinese(Simplified)", value="zh-cn"),
        app_commands.Choice(name="Chinese(Traditional)", value="zh-tw"),
        app_commands.Choice(name="Spanish", value="es"),
        app_commands.Choice(name="French", value="fr"),
        app_commands.Choice(name="Vietnamese", value="vi"),
        app_commands.Choice(name="Thai", value="th"),
        app_commands.Choice(name="Indonesia", value="id"),
        ])
@app_commands.describe(
    show='defalut false'
)
async def translate(interaction: discord.Interaction, message: str, transfrom: app_commands.Choice[str], transto: app_commands.Choice[str], show: bool):
    """Translate this message"""
    
    result = await translator(message, transfrom, transto, show)
    if show:
        await interaction.response.send_message(result)
    else:
        await interaction.response.send_message(result,ephemeral=True)

async def translator(message, transfrom, transto, show):

    From = transfrom.value
    To = transto.value

    if transfrom.value == "zh-tw":
        From = "zh-TW"
    elif transfrom.value == "zh-cn":
        From = "zh-CN"

    if transto.value == "zh-tw":
        To = "zh-TW"
    elif transto.value == "zh-cn":
        To = "zh-CN"

    try:
        #response = translator.translate('안녕하세요', 'ko', 'zh-TW')
        #print(response)
        response = PAPAGO.translate(message, From, To)

        if show:
            return response.text
        else:
            return "\"" + message + "\"\n" +transfrom.name +"→"+ transto.name + "\n\"" + response.text + "\""
        
    except Exception as e:
        return "Something went wrong. Please try again later ;_;\nIf the problem keeps happening, please contact the server owner."
        #return repr(e)


client.run(os.environ['DISCORD_BOT_TOKEN'])