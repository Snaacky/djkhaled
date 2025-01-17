import discord
from discord.ext import commands


async def send_embed(ctx: commands.Context, title: str, description: str, color: discord.Color):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


async def send_error(ctx: commands.Context, description: str):
    await send_embed(ctx=ctx, title="❌ Error", description=description, color=discord.Color.red())
