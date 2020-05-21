import discord
from discord.ext import commands
# from discord.ext.commands import has_permissions,CheckFailure
# import asyncio

import time
import datetime


class Cog(commands.Cog):
    hidden = False
    def __init__(self, client, *args, **kwargs):
        self.client = client
        self.logger = self.client.logger
        super().__init__(*args, **kwargs)

    def error(self, ctx, msg, desc):
        embed=discord.Embed(title=msg, description=desc, colour=self.client.config["colour"]["error"])
        return ctx.send(embed=embed)


class Events(Cog):
    hidden=True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="Bot online."))
        self.logger.info("Bot Online\nName : %s\nID: %s"%(self.client.user.name, self.client.user.id))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author != self.client.user: return
        if len(msg.embeds) == 0: return
        if msg.embeds[0].title == "Pong!":
            delay = round(float("0.%s"%str(msg.created_at - datetime.datetime.now()).split(".")[1])*1000, 2)
            await msg.edit(embed=discord.Embed(title="Pong!", description="Delay: %sms"%delay, colour=self.client.config["colour"]["success"]))




class Information(Cog):
    """Information commands."""

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Ping the bot."""
        await ctx.send(embed=discord.Embed(title="Pong!", colour=self.client.config["colour"]["success"]))

    @commands.command(pass_context=True, aliases=["credit","devs"])
    async def credits(self, ctx):
        """Who made the bot."""
        embed=discord.Embed(colour=self.client.config["colour"]["success"])
        embed.set_author(name=self.client.user.name, icon_url=self.client.get_user(self.client.user.id).avatar_url)
        embed.add_field(name="**Developers**", value="\n".join(["<@%s>"%x for x in self.client.config["devs"]]), inline=False)
        embed.add_field(name="**Assistants**", value="\n".join(["<@%s>"%x for x in self.client.config["asshelp"]]), inline=False)
        embed.set_footer(text="%s | %s"%(self.client.user.name, datetime.datetime.utcfromtimestamp(time.time())), icon_url=self.client.get_user(self.client.user.id).avatar_url)
        await ctx.send(embed=embed)

    def gen_help(self, cog):
        halp = discord.Embed(title="%s - %s" %(cog, self.client.cogs[cog].__doc__) , description="Commands.", colour=self.client.config["colour"]["help"])

        for c in self.client.get_cog(cog).get_commands():
            if not c.hidden:
                halp.add_field(name=c.name,value=c.help, inline=False)

        return halp


    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, command=None):
        """Gives help on how to use commands."""
        try:
            if not command:
                for cog in self.client.cogs:
                    if self.client.get_cog(cog).hidden: continue
                    await ctx.send(embed=self.gen_help(cog))
                return
            else:
                cm = self.client.get_command(command)

                if cm == None:
                    a = {}
                    for i in self.client.cogs:
                        a[i.lower()] = i

                    print(a)

                    if self.client.get_cog(a.get(command.lower(), None)) == None: return await self.error(ctx, "Invalid data", "Data '%s' was not recogniesed as command or category.\nUsage `%shelp %s`"%(command, self.client.command_prefix, self.client.get_command("help").signature))
                    return await ctx.send(embed=self.gen_help(a.get(command.lower(), None)))

                halp = discord.Embed(title="%s - %s" %(cm.name, cm.help), colour=self.client.config["colour"]["help"])
                halp.add_field(name="Usage", value="%s%s %s"%(self.client.command_prefix, command, cm.signature))
                halp.add_field(name="Aliases", value=(", ".join(cm.aliases)) if len(cm.aliases) > 0 else "None")
                return await ctx.send(embed=halp)

        except Exception as e:
            self.client.logger.error(e)
            raise e
            return await ctx.send("Excuse me, I can't send embeds.")
