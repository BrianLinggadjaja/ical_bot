import discord
import requests
import re
import asyncio
import os
from datetime import datetime

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.print_todays_birthdays())

    async def on_message(self, message):
        if message.author == self.user:
            return
            
        if message.content == '!ping':
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

                if (currentFormatted24Hour >= startFormatted24Hour) and (currentFormatted24Hour <= endFormatted24Hour):
                    currentFormattedHour=''.join(currentFormattedHour)
                    startFormattedHour=''.join(startFormattedHour)
                    endFormattedHour=''.join(endFormattedHour)

                    for guild in self.guilds:
                        for channel in guild.channels:
                            await message.channel.send(channel)
                            
                        return

                    # await message.channel.send('> **Only Cams Access** has started! \n > Join the video call *NOW* from **' + startFormattedHour + '** to **' + endFormattedHour + '**')
                    # return

    def convert_12_to_24_hour(self, timeArray):
        hour = int(timeArray[0])
    
        if timeArray[1].lower() == 'pm':
            hour += 12

        return hour

    async def print_todays_birthdays(self):
        await self.wait_until_ready()

        while not self.is_closed():
            currentDateTime=datetime.now()
            currentDay=currentDateTime.strftime('%A').lower()
            postDay=os.environ['POST_DAY'].lower()

            if currentDay == postDay:
                currentHour=currentDateTime.strftime('%-I %p')
                startHour=os.environ['START_HOUR']
                endHour=os.environ['END_HOUR']
                await message.channel.send('Only Cams now Active')
                return

                for guild in self.guilds:
                        for channel in guild.channels:
                            if str(channel) == "🎁birthdays" or str(channel) == "general":
                                await channel.send('test')

            await asyncio.sleep(3600)

client = MyClient()
client.run(os.environ['ACCESS_TOKEN'])
