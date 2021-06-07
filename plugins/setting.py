from pyrogram import Client, filters 
from gpyts.asyncGpyts import Gpyts
from config import strings, db
from onion import peer
import asyncio, re, os
import pyrogram 


@Client.on_message(filters.command(['lists', 'list']) & filters.private)
async def lists(client, message):
	user = peer()
	await user.init(db, message.from_user.id)
	languages = await Gpyts().iso(True)
	data = strings.key('lang_list', user.js['mylang'])
	for key in languages.get('gts').keys():
		data += f"\n {key} : <code>{languages['gts'][key]}</code>" 
	await message.reply(data)

@Client.on_message(filters.command(['tolang', 'defaultlang']) & filters.private)
async def lang(client, message):
	user = peer()
	await user.init(db, message.from_user.id)
	languages = await Gpyts().iso()
	if len(message.text.split()) == 2 and message.text.split()[1] in languages['gts']:
		await user.tolang(message.text.split()[1])
		await message.reply(strings.key('sepa_done', user.js['mylang']).format(user.js['tolang']))
	else:
		await message.reply(strings.key('to_lang', user.js['mylang']).format(user.js['tolang']))
	

@Client.on_message(filters.command(['sepa', 'separator']) & filters.private)
async def sepa(client, message):
	symbols = ('~','!','@','#','$','%','^','&','*','_','+','=','-',':',';','?','>','|','.')
	user = peer()
	await user.init(db, message.from_user.id)
	if len(message.text.split()) == 2 and message.text.split()[1] in symbols:
		await user.sepa(message.text.split()[1])
		await message.reply(strings.key('sepa_done', user.js['mylang']).format(user.js['sepa']))
	else:
		await message.reply(strings.key('sepa_404', user.js['mylang']).format(user.js['sepa']))
