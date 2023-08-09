import discord
from discord.ext import commands
from datetime import datetime, timezone
import humanize

class Dictatortime(commands.Cog):
    def __init__(self, lyrabot):
        self.lyrabot = lyrabot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dictatortime is ready")

    """Some time ago I asked about the format the datebase time is in. I wanted to know what format the date
    arrives as before you convert it to something usable. I have used a random date pulled from what you showed me,
    for all of my testing. As I don't have access to the database and have no idea how to do a fake one, I can only assume
    that this will work and can't test further. It has worked in all of my tests in its current form.

    Also obviously my bot doesn't have slash commands yet. The relevent changes to the code don't really include anything
    that changes with slash commands. Mostly only leaving in command format so it won't throw errors at me, and because I was testing.
    """


    # The version with the least changes. One less line of code to get current time, and last_active loses the longer line.
    @commands.command()
    async def split(self, ctx):
        last_active = datetime.strptime("2022-03-17 00:00:00", '%Y-%m-%d %H:%M:%S')
        last_active = last_active.replace(tzinfo=timezone.utc)
        diff = discord.utils.utcnow() - last_active
        diff_split = str(diff).split(':')
        diff_formatted = f'{diff_split[0]} hours, {diff_split[1]} minutes ago'
        # diff_split[0] appears as '3 days, 4' where 3 = amount of days and 4 = amount of hours.

        # tested that this code will work as I expected once it's in an embed, with this simple example
        embed = discord.Embed(title="Time Test", description="Making sure this works in an embed", colour=discord.Colour.dark_gold())
        embed.add_field(name="How Long", value=diff_formatted, inline=True)
        await ctx.send(embed=embed)


    # When researching the best way to display the timedelta in a nice format, many people recommended the humanize module.
    # The is my experiment with that. Without all the extra code, precisedelta would display way too much information.
    @commands.command()
    async def humanizeprecise(self, ctx):
        now = discord.utils.utcnow()
        last_active = datetime.strptime("2022-03-17 00:00:00", '%Y-%m-%d %H:%M:%S')
        last_active = last_active.replace(tzinfo=timezone.utc)
        delta = now - last_active
        # for a month or more, display years, months and days (or months and days if no years):
        if delta.total_seconds() >= 30 * 24 * 60 * 60:
            diff = humanize.precisedelta(now - last_active, minimum_unit="days", format="%.0f")
        # for less than a month at least 1 day, display days and hours:
        elif delta.total_seconds() >= 24 * 60 * 60:
            diff = humanize.precisedelta(now - last_active, minimum_unit="hours", format="%.0f")
        # for less than 1 day and more that 1 minute, display hours and minutes (or only minutes):
        elif delta.total_seconds() >= 60 * 60:
            diff = humanize.precisedelta(now - last_active, minimum_unit="minutes", format="%.0f")
        # if less than a minute, display seconds:
        else:
            diff = humanize.precisedelta(now - last_active, minimum_unit="seconds", format="%.0f")
        await ctx.send(f"{diff} ago")   
# eg:
# if years - 2 years, 5 months and 3 days ago
# if months - 5 months and 3 days ago
# if days - 3 days and 12 hours ago
# if hours - 12 hours and 34 minutes ago
# if minutes - 34 minutes ago
# if seconds - 32 seconds ago


    # humanize does also have a method which displays things in a simpler format including things like "a moment ago"
    # The problem with this method is it loses a lot of accuracy. Eg my time since joining my test discord is 1 month, 16 days, but this method just shows "a month ago"
    @commands.command()
    async def humanizenatural(self, ctx):
        now = discord.utils.utcnow()
        last_active = datetime.strptime("2022-03-17 00:00:00", '%Y-%m-%d %H:%M:%S')
        last_active = last_active.replace(tzinfo=timezone.utc)
        difference = humanize.naturaltime(now - last_active)
        await ctx.send(f"{difference}")



    # finally, for interest sake, this was the start of my attempt to do the nice formatting myself (and just learn more), wohhout the help of humanize.
    # So far I just have the information I would need. A lot of if/else statements still to be written with this meethod.
    @commands.command()
    async def myformat(self, ctx, member:discord.Member = commands.Author):
        delta = discord.utils.utcnow() - member.joined_at
        days = (delta.days)
        hours = (delta.seconds // 3600) % 24
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds % 60
        
        await ctx.send(f"The time difference is {days} days, {hours} hours, {minutes} minutes and {seconds} seconds.")


async def setup(lyrabot):
    await lyrabot.add_cog(Dictatortime(lyrabot))