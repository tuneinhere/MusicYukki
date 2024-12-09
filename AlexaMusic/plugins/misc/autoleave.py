# Copyright (C) 2024 by Alexa_Help @ Github, < https://github.com/TheTeamAlexa >
# Subscribe On YT < Jankari Ki Duniya >. All rights reserved. © Alexa © Yukki.

""""
TheTeamAlexa is a project of Telegram bots with variety of purposes.
Copyright (c) 2024 -present Team=Alexa <https://github.com/TheTeamAlexa>

This program is free software: you can redistribute it and can modify
as you want or you can collabe if you have new ideas.
"""

import asyncio
from pyrogram.enums import ChatType
from datetime import datetime, timedelta

import config
from AlexaMusic import app
from AlexaMusic.core.call import Alexa
from AlexaMusic.utils.database import (
    get_client,
    is_active_chat,
    is_autoend,
    get_assistant,
)

autoend = {}


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME):
            from AlexaMusic.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                try:
                    async for i in client.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if (
                                chat_id != config.LOG_GROUP_ID
                                and chat_id != -1002367211578
                            ):
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                    except:
                                        continue
                except:
                    pass


asyncio.create_task(auto_leave())


async def auto_end():
    while True:
        await asyncio.sleep(30)
        for chat_id, timer in list(autoend.items()):
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    del autoend[chat_id]
                    continue
                userbot = await get_assistant(chat_id)
                members = []
                async for member in userbot.get_call_members(chat_id):
                    if member is None:
                        continue
                    members.append(member)
                if len(members) <= 1:
                    try:
                        await Alexa.stop_stream(chat_id)
                    except Exception:
                        pass
                    try:
                        await app.send_message(
                            chat_id,
                            "Udah ga demus kan anj? yaudah gua cabut.",
                        )
                    except Exception:
                        pass
                del autoend[chat_id]


asyncio.create_task(auto_end())
