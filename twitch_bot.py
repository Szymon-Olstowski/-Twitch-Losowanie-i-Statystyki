from twitchio.ext import commands
import sqlite3,os
from dotenv import load_dotenv
import os
load_dotenv()
DB_NAME = "users.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
                 (username text PRIMARY KEY, streamer text)"""
    )
    conn.commit()
    conn.close()

def add_user(username, streamer):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username, streamer) VALUES (?, ?)", (username, streamer))
    user_added = c.rowcount > 0  
    conn.commit()
    conn.close()
    return user_added

create_db()  

def read_channel_names():
    with open('channels.txt', 'r') as file:
        streamers = [line.strip() for line in file if line.strip()] 
    return streamers
CHANNEL_NAMES = read_channel_names()
class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.getenv('TOKEN'), prefix= os.getenv('PREFIX'), initial_channels=CHANNEL_NAMES)
        self.running = False
    async def event_ready(self):
        print('Bot uruchomiony')
    @commands.command(name='los')
    async def los(self, ctx):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT status FROM status")
        t = c.fetchone()
        channel_name = ctx.channel.name
        if str(t) == str("('OK',)"):
            if add_user(ctx.author.name, channel_name): 
                print(f"Dodano użytkownika do bota: {ctx.author.name} z kanału {channel_name}")
            else:
                await ctx.send(f'{ctx.author.name} już bierze udział w losowaniu')
        if str(t) == str("('STOP',"):
            await ctx.send(f'{ctx.author.name} wyłączona komenda do losowania')
            print('Wyłączona komenda do losowania')
        conn.close()

    def start_bot(self):
        self.running = True
        global CHANNEL_NAMES  
        CHANNEL_NAMES = read_channel_names() 
        self.run()
        

    async def stop_bot(self):
        await self.close()
        self.running = False
bot = TwitchBot()