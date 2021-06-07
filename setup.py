#!/usr/bin/python3
from db import litedb
from onion import peer
from strings import strings
from pyrogram import Client, idle
import asyncio, logger
import config

app = Client("tltebot")
async def main():
    config.init()
    config.db = litedb()
    config.strings = strings()
    config.ADMIN = [521485281]
    await config.db.connect('./db/tandora', assoc = True)
    await app.start()
    await idle()
if __name__ == '__main__' :
	app.run(main())