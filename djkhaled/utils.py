import discord


async def send_embed(self, ctx, title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


async def send_error(self, ctx, description):
    send_embed(ctx=ctx, title="❌ Error", description=description, color=discord.Color.red())
