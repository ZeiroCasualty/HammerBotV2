import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import schedule
import tracemalloc
import asyncio
from datetime import datetime

# Load environment variables from a .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

tracemalloc.start()

# Bot setup
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Dictionary to store members and their tasks
members_tasks = {
    1297751702019113081: ["Cook - Breakfast", "Cook - Lunch", "Organize Dishes / Cook Rice", "Wash Dishes - Breakfast", "Cook - Breakfast"],  #Yasmin
    182703599397240832: ["Wash Dishes - Lunch (Outdoor)", "Set/Clean Table/Leftovers", "Wash Dishes - EOD", "Organize Dishes / Cook Rice", "Wash Dishes - Lunch (Indoor)"], #Bernie
    1297750232745902196: ["Set/Clean Table/Leftovers", "Cook - Breakfast", "Cook - Lunch", "Cook - Breakfast", "Cook - Lunch"], #Dani
    1297749519559299102: ["Wash Dishes - Lunch (Indoor)", "Wash Dishes - EOD", "Set/Clean Table/Leftovers", "Wash Dishes - Lunch (Outdoor)", "Organize Dishes / Cook Rice"], #Justin
    1297749741190385736: ["Wash Dishes - Breakfast", "Wash Dishes - Lunch (Indoor)", "Wash Dishes - Lunch (Outdoor)", "Set/Clean Table/Leftovers", "Wash Dishes - EOD"], #Jen
    1297749740489936939: ["Organize Dishes / Cook Rice", "Wash Dishes - Breakfast", "Wash Dishes - Lunch (Indoor)", "Wash Dishes - EOD", "Set/Clean Table/Leftovers"], #Jessa
    1297752200767868993: ["Cook - Lunch", "Wash Dishes - Lunch (Outdoor)", "Cook - Breakfast", "Cook - Lunch", "Wash Dishes - Breakfast"], #Darling
    1297749642230104125: ["Wash Dishes - EOD", "Organize Dishes / Cook Rice", "Wash Dishes - Breakfast", "Wash Dishes - Lunch (Indoor)", "Wash Dishes - Lunch (Outdoor)"], #Cris
}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    assign_tasks.start()  # Starts the task assignment loop

@tasks.loop(minutes=1)
async def assign_tasks():
    # Run only on weekdays
    if datetime.today().weekday() < 5:  # 0-4 are Mon-Fri
        # Schedule to send task at a specific time (e.g., 8 AM)
        schedule.every().day.at("7:00").do(assign_member_tasks)

        # Run the scheduled job in async
        await assign_member_tasks()
        await run_schedule()

async def assign_member_tasks():
    # Get today's weekday index (0=Monday, 4=Friday)
    day_index = datetime.today().weekday()
    
    # Assign tasks to each member in the members_tasks dictionary
    for member_id, task_list in members_tasks.items():
        if day_index < len(task_list):  # Ensure there's a task for today
            task = task_list[day_index]
            member = await bot.fetch_user(member_id)  # Fetch the member by ID
            if member:
                await member.send(f"Today's task: {task}")

async def run_schedule():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  # Check every minute

# Run the bot with the token from the .env file
bot.run(TOKEN)
