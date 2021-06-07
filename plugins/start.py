from  pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from config import strings, db
from onion import peer
import asyncio, re, os


@Client.on_message(filters.regex('start') & filters.private)
async def start(client, message):
    user = peer()
    await user.init(db, message.from_user.id)
    await message.reply(
    	strings.key('start', user.js['mylang']).format(message.from_user.first_name), 
    	reply_markup = InlineKeyboardMarkup([
    		[InlineKeyboardButton(text = 'Try me inline ☁️', switch_inline_query_current_chat = f"This is a test 🐈 {user.js['sepa']}ja")],
    		[InlineKeyboardButton(text = 'Source 🗂', url='https://github.com/Ripeey/Tltebot')]
    		]) 
    	)

@Client.on_message(filters.command('help') & filters.private)
async def help(client, message):
	user = peer()
	await user.init(db, message.from_user.id)
	await message.reply(strings.key('help', user.js['mylang']).format(message.from_user.first_name))
