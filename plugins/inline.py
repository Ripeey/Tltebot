from pyrogram import Client, filters 
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from gpyts.asyncGpyts import Gpyts
from config import strings, db
from onion import peer
import asyncio, re, os
import pyrogram 

gpyts = Gpyts()

@Client.on_inline_query(filters.regex(r'^$'))
async def inline_empty(client, inline):
	await inline.answer([], cache_time = 0, switch_pm_text = 'How does this works | source (?)', switch_pm_parameter = 'tesfk')

@Client.on_inline_query(filters.regex(r'.+'))
async def inline_start(client, inline):
	user = peer()
	await user.init(db, inline.from_user.id)
	languages = await gpyts.iso()
	if inline.query.startswith(user.js['sepa'], -3) and inline.query[-2:] in languages['gts']:
		lang = inline.query[-2:] 
		payload = inline.query[:-3]
		cache = 999
	else:
		lang = user.js['tolang'] # default en
		payload = inline.query
		cache = 9
	user = peer()
	await user.init(db, inline.from_user.id)

	# result fill-up
	result = []
	payout_text = (await gpyts.translate(payload, to_lang = lang)).text
	result.append(await InlineQueryResultArticle(id = 'tl_text', title = 'Translate to {} text'.format(lang), description = payout_text, input_message_content = InputTextMessageContent(message_text = payout_text), thumb_url = 'https://i.imgur.com/gyFLucU.png').write(client))
	if lang in languages['tts']:
		voice_1 = (await gpyts.tts(payout_text, lang, False)).file
		voice_2 = (await gpyts.tts(payload, lang, False)).file
		result.append( pyrogram.raw.types.InputBotInlineResult(id = 'tl_voice', type = 'voice', send_message = pyrogram.raw.types.InputBotInlineMessageMediaAuto(message = ""), title = 'Translate to {} voice'.format(lang), description = 'send {} translation voice'.format(lang), thumb = pyrogram.raw.types.InputWebDocument(url = 'https://i.imgur.com/vZNJBrc.png', size = 0, mime_type="image/gif", attributes = []), content = pyrogram.raw.types.InputWebDocument(url = str(voice_1), size = 0, mime_type="audio/mp3", attributes = []) ))
		result.append( pyrogram.raw.types.InputBotInlineResult(id = 'ct_voice', type = 'voice', send_message = pyrogram.raw.types.InputBotInlineMessageMediaAuto(message = ""), title = 'Convert text to voice'.format(lang), description = 'send converted voice'.format(lang), thumb = pyrogram.raw.types.InputWebDocument(url = 'https://i.imgur.com/Ued66CI.png', size = 0, mime_type="image/gif", attributes = []), content = pyrogram.raw.types.InputWebDocument(url =  str(voice_2), size = 0, mime_type="audio/mp3", attributes = []) ))

	# result dispatch
	await Client.send(client, data = pyrogram.raw.functions.messages.SetInlineBotResults(
		query_id = int(inline.id), 
		cache_time = cache,
		results = result, 
		gallery = False,
		private = True,
		switch_pm = pyrogram.raw.types.InlineBotSwitchPM(text = 'How does this works | source (?)', start_param = 'tesfk')
		))
