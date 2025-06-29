import discord
from discord.ext import commands
import json
import hashlib
import random

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

# Save config
def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

# Fake dice game (always returns the opposite)
@bot.command()
async def dice(ctx, arg=None):
    if arg != "2x":
        await ctx.send("Usage: `$dice 2x`")
        return

    # Simulate roll (based on server seed and random salt)
    salt = str(random.randint(100000, 999999))
    roll_input = config["server_seed"] + salt
    hashed = hashlib.sha256(roll_input.encode()).hexdigest()
    roll = int(hashed[:8], 16) % 10000 / 100  # 0.00 to 99.99

    # Determine loss (opposite logic)
    result = "❌ You lost!" if roll < 50 else "✅ You won!"  # BUT FLIPPED BELOW
    forced_result = "✅ You won!" if result == "❌ You lost!" else "❌ You lost!"  # Reverse

    await ctx.send(
        f"🎲 Roll: **{roll:.2f}**\nResult: **{forced_result}**"
    )

# Set seed (admin only or for test)
@bot.command()
async def setseed(ctx, *, seed: str):
    config["server_seed"] = seed
    save_config()
    await ctx.send(f"🔒 Server seed has been updated.")

bot.run(config["token"])
  
