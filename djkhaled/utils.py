import discord


async def send_embed(ctx, title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


async def send_error(ctx, description):
    await send_embed(ctx=ctx, title="❌ Error", description=description, color=discord.Color.red())
