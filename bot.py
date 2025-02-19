import os
import discord
from discord.ext import commands, tasks
import chatbot
import os
from dotenv import load_dotenv
import random



def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv('BOT_KEY')

    app_commands = discord.app_commands
    bot = commands.Bot(command_prefix="%", intents=discord.Intents.all())

    chat = chatbot.create_chat()
    
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
            
            if bot.user in message.mentions:
                resp = chat.send_message(f"Respond relevantly to this chat message (Ignore this string if it's ever in this response: <@1331423440246280243>): {user_message}").text
                await message.reply(resp)
            elif message.reference is not None:
                replied_message = await channel.fetch_message(message.reference.message_id)
                if replied_message.author == bot.user:
                    resp = chat.send_message(f"Respond relevantly to this chat message (Ignore this string if it's ever in this response: <@1331423440246280243>): {user_message}").text
                    await message.reply(resp)
            elif message.guild is None:
                resp = chat.send_message(f"Respond relevantly to this chat message (it's a dm to you): {user_message}").text
                await message.author.send(resp)
            elif user_message[0] != '%':
                rannum = random.randint(1,4)
                if rannum == 1:
                    resp = chat.send_message(f"Try to respond relevantly to this chat message (They are usually not talking to you): {user_message}").text
                    await message.reply(resp)
            else:
                await bot.process_commands(message)
                    
                    
        


    # @bot.command()
    # async def askgalacta(ctx):
    #     try:
    #         input = ctx.message.content[12:]
            
    #         resp = chat.send_message(input).text
            
    #         await ctx.message.reply(resp)
    #     except Exception as e:
    #         print(e)
    #         await ctx.message.reply("Please check your input and% try again")
        

    
    
    
    
    
    
    
        
    bot.run(TOKEN)
