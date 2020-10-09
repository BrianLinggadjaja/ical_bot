import discord
import requests
import re
import asyncio
import os
from datetime import datetime

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.toggle_notify_access())

    async def toggle_notify_access(self):
        await self.wait_until_ready()

        hasNotified=False
        # todo: refactor this multiple methods
        while not self.is_closed():
            currentDateTime=datetime.now()
            currentDay=currentDateTime.strftime('%A').lower()
            postDay=os.environ['POST_DAY'].lower()

            if currentDay == postDay:
                currentHour=currentDateTime.strftime('%-I %p')
                currentFormattedHour=currentHour.split(' ')
                currentFormatted24Hour=self.convert_12_to_24_hour(currentFormattedHour)
                startHour=os.environ['START_HOUR']
                startFormattedHour=startHour.split(' ')
                startFormatted24Hour=self.convert_12_to_24_hour(startFormattedHour)
                endHour=os.environ['END_HOUR']
                endFormattedHour=endHour.split(' ')
                endFormatted24Hour=self.convert_12_to_24_hour(endFormattedHour)

                for guild in self.guilds:
                        for channel in guild.channels:
                            targetChannel=os.environ['TARGET_CHANNEL']

                            if (currentFormatted24Hour >= startFormatted24Hour) and (currentFormatted24Hour <= endFormatted24Hour) and not hasNotified:
                                notifyChannel=os.environ['NOTIFY_CHANNEL']

                                if str(channel) == targetChannel:
                                    userLimit=os.environ['MAX_CONNECTIONS']
                                    
                                    await channel.edit(user_limit=userLimit)
                                    await channel.set_permissions(guild.default_role, connect=True)
                                elif str(channel) == notifyChannel:
                                    currentFormattedHour=''.join(currentFormattedHour)
                                    startFormattedHour=''.join(startFormattedHour)
                                    endFormattedHour=''.join(endFormattedHour)

                                    await channel.send('> **Only Cams Access** has started! \n > Join the video call *NOW* from **' + startFormattedHour + '** to **' + endFormattedHour + '**')
                                
                                hasNotified=True
                            else:
                                if str(channel) == targetChannel:
                                    await channel.edit(user_limit=0)
                                    await channel.set_permissions(guild.default_role, connect=False)
                        
                                hasNotified=False

                await asyncio.sleep(60)

    def convert_12_to_24_hour(self, timeArray):
        hour = int(timeArray[0])
    
        if timeArray[1].lower() == 'pm':
            hour += 12

        return hour

client = MyClient()
client.run(os.environ['ACCESS_TOKEN'])
