import os
import discord
from discord.ext import commands, tasks
import api_responses
import os
from dotenv import load_dotenv

import heroinfo


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('BOT_KEY')

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready")
        try:
            await bot.tree.sync()
        except Exception as e:
            print(e)

    #Sample Code to refer to:

    # @bot.tree.command(name='masteryna', description='Get Player Mastery Info Based on Summoner ID.')
    # @app_commands.describe(name = "Summoner Name", tag = "Summoner Tag number after the # (Ex: '0001')")
    # async def masteryna(interaction: discord.Interaction, name: str, tag: int):
    #     await interaction.response.defer()



    #     result = api_responses.getMastery(name, tag)

    #     output = f"**Here are the top 3 highest mastery champions of {name}#{tag}:**\n\n\n"


    #     for i in range(3):
    #         champ = api_responses.get_champion_by_key(result[i]["championId"])
    #         try:
    #             output += f"#{i+1}: {champ["id"]}, \"{champ["title"]}\" \nMastery Level: {result[i]["championLevel"]} ({result[i]["championPoints"]} pts.) https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ["id"]}_0.jpg \n\n"
    #         except Exception as e:
    #             print(e)

    #     await interaction.followup.send(output)
    
    @bot.tree.command(name='Hero Info', description='Lists Information of a specific hero')
    @app_commands.describe(name = "Hero")
    async def heroinfo(interaction: discord.Interaction, name: str):
        try:
            await interaction.send_message(heroinfo.getBasic(name))
        except Exception as e:
            print(e)
            await interaction.response.send_message("Failed")
        
    
    
    
    
    
    
    
    
        
    bot.run(TOKEN)
