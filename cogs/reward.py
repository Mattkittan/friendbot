import discord
import re
from discord.ext import commands
from bfunc import roleArray, calculateTreasure, timeConversion, commandPrefix, tier_reward_dictionary

class Reward(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, type=commands.BucketType.member)
    @commands.command()

    async def reward(self,ctx, timeString=None, tier=None):
        rewardCommand = f"\nPlease follow this format:\n```yaml\n{commandPrefix}reward \"#h#m\" \"tier\"```\n"

        def convert_to_seconds(s):
            return int(s[:-1]) * seconds_per_unit[s[-1]]

        channel = ctx.channel
        if timeString is None:
            await channel.send(content="Woops, you're forgetting the time duration for the command." + rewardCommand)
            return

        if tier is None:
            await channel.send(content="Woops, you're forgetting the tier for the command. Please try again with 1, 2, 3, or 4 or Junior, Journey, Elite, or True as the tier, and" + rewardCommand)
            return

        seconds_per_unit = { "m": 60, "h": 3600 }
        lowerTimeString = timeString.lower()

        if tier not in ('0','1','2','3','4', '5') and tier.lower() not in [r.lower() for r in roleArray]:
            await channel.send(f"`{tier}` is not a valid tier. Please try again with 0, 1, 2, 3, 4, 5 or New, Junior, Journey, Elite, True or Ascended.")
            return

        tierName = ""
        if tier.isdigit():
            tierName = roleArray[int(tier)]
            tier = tierName
        else:
            tierName = tier.capitalize()
        print(tierName)
        l = list((re.findall('.*?[hm]', lowerTimeString)))
        totalTime = 0
        for timeItem in l:
            totalTime += convert_to_seconds(timeItem)

        if totalTime == 0:
            await channel.send(content="You may have formatted the time incorrectly or calculated for 0. Try again with the correct format." + rewardCommand)
            return

        cp = ((totalTime) // 1800) / 2
        tier = tier.lower()
        t = 0
        if tier == 'junior':
          t = 0
        elif tier == "journey":
          t = 1
        elif tier == "elite":
          t = 2
        elif tier == "true":
          t = 3
        elif tier == "ascended":
          t = 4
        
        gp = cp* tier_reward_dictionary[t][0]
        tp = cp* tier_reward_dictionary[t][1]
        

        treasureArray = [cp, tp, gp]
        durationString = timeConversion(totalTime)
        treasureString = f"{treasureArray[0]} CP, {treasureArray[1]} TP, and {treasureArray[2]} GP"
        await channel.send(content=f"A {durationString} game would give a **{tierName}** Friend\n{treasureString}")
        return

def setup(bot):
    bot.add_cog(Reward(bot))
