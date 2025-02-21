import os
import discord
from discord.ext import commands, tasks
import chatbot
import os
from dotenv import load_dotenv
import random
import heroinfo
import datetime



def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('BOT_KEY')

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())
    bot.remove_command("help")

    chat = chatbot.create_chat()
    HISTORY_FILE = "conversation_history.txt"
    
    def save_history(username, user_message, bot_response):
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username}: {user_message}\n")
            f.write(f"Bot: {bot_response}\n")
    
    
    
    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready")
        try:
            await bot.tree.sync()
        except Exception as e:
            print(e)
            
    @bot.event
    async def on_message(message):
        if message.author != bot.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}' ({channel})")
            if user_message[0] != '%':
                if bot.user in message.mentions:
                    resp = chat.send_message(f"Respond relevantly to this chat message from a chatter,{username}, talking to you (<@1331423440246280243> is your ping, ignore it and avoid using it in your message): {user_message}").text
                    await message.reply(resp)
                    save_history(username, user_message, resp)
                elif message.reference is not None:
                    replied_message = await message.channel.fetch_message(message.reference.message_id)
                    if replied_message.author == bot.user:
                        resp = chat.send_message(f"Respond relevantly to this chat message from a chatter, {username}, talking to you): {user_message}").text
                        await message.reply(resp)
                        save_history(username, user_message, resp)
                elif message.guild is None:
                    resp = chat.send_message(f"Respond relevantly to this chat message (it's a dm to you): {user_message}").text
                    await message.author.send(resp)
                    save_history(username, user_message, resp)
                else:
                    rannum = random.randint(1,100)
                    print(rannum)
                    if rannum >= 80:
                        resp = chat.send_message(f"Try to respond relevantly to this chat message (They are usually not talking to you): {user_message}").text
                        await message.reply(resp)
                        save_history(username, user_message, resp)
                    elif rannum == 1:
                        resp = chat.send_message(f"Make up a random reason to timeout this chatter, {username}, for 5 minutes based on their message: {user_message}").text
                        await message.reply(resp)
                        await message.author.timeout(datetime.timedelta(minutes=5),reason = resp)
                        
            else:
                await bot.process_commands(message)
            
                    
                    
    @bot.command()
    async def help(ctx):
        await ctx.message.reply("**%playerinfo:** Use %playerinfo [Marvel Rivals Username] to get an overview of your Marvel Rivals (S1) stats.")


    @bot.command()
    async def playerinfo(ctx):
        try:
            input = ctx.message.content[12:]
                        
            response = heroinfo.getbasicInfo(input)
            
            embed = discord.Embed(
            title=f"Season 1 stats for: {response['player_name']}",
            description=f"Current Rank: **{response['stats']['rank']['rank']}**",
            color=discord.Color.yellow()
            )
            embed.add_field(name="Level: ", value=f"**{response['stats']['level']}**", inline=True)
            embed.add_field(name="Total Matches", value=f"**{response['stats']['total_matches']}**", inline=False)
            embed.add_field(name="Win Rate", value=f"**{str(round((float(response['stats']['total_wins'])/float(response['stats']['total_matches']) * 100), 2))}%**", inline=False)
            try:
                embed.set_thumbnail(url=f'{heroinfo.getPic(response["player_icon_id"])}')
                await ctx.message.reply(embed=embed)
            except Exception as e:
                print(e)
                await ctx.message.reply(embed=embed)
            
            

        except Exception as e:
            print(e)
            await ctx.message.reply("Player not found.")
        
        

    
    
    
    
    
    
    
        
    bot.run(TOKEN)
