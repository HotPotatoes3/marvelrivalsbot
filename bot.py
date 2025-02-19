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
    HISTORY_FILE = "conversation_history.txt"
    
    def save_history(username, user_message, bot_response):
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username}: {user_message}\n")
            f.write(f"Bot: {bot_response}\n")

    # Function to load conversation history (for learning)
    def load_history():
        history = ""
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = f.read()
        return history
    
    
    
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
                resp = chat.send_message(f"Respond relevantly to this chat message from a chatter,{username}, talking to you (<@1331423440246280243> is your ping, ignore it and avoid using it in your message): {user_message}").text
                await message.reply(resp)
                save_history(username, user_message, resp)
            elif message.reference is not None:
                replied_message = await channel.fetch_message(message.reference.message_id)
                if replied_message.author == bot.user:
                    resp = chat.send_message(f"Respond relevantly to this chat message from a chatter, {username}, talking to you): {user_message}").text
                    await message.reply(resp)
                    save_history(username, user_message, resp)
            elif message.guild is None:
                resp = chat.send_message(f"Respond relevantly to this chat message (it's a dm to you): {user_message}").text
                await message.author.send(resp)
                save_history(username, user_message, resp)
            elif user_message[0] != '%':
                rannum = random.randint(1,5)
                if rannum == 1:
                    resp = chat.send_message(f"Try to respond relevantly to this chat message (They are usually not talking to you): {user_message}").text
                    await message.reply(resp)
                    save_history(username, user_message, resp)
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
