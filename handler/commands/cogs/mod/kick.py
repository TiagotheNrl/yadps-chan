from handler.config.data import Data
from disnake.ext import commands
import disnake as discord

class Kick(commands.Cog):

    data = Data()

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.slash_command(description="Ping bot")
    @commands.has_any_role(data.config["modRoleId"], data.config["adminRoleId"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def kick(self, ctx, user: discord.User):
        try:
            await ctx.guild.kick(user=user)
            await ctx.channel.send(f"{user} has been kicked by: {ctx.author.mention}")
        except (discord.ext.commands.UserInputError, discord.ext.commands.UserNotFound) as err:
            await ctx.channel.send(f"{ctx.author.mention}, you need to specify the user to kick!")
            return


def setup(bot):
    bot.add_cog(Kick(bot))
