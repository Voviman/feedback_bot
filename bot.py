import os
from urllib.parse import urljoin

import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType
from aiogram.dispatcher.webhook import get_new_configured_app

TOKEN = ''
PROJECT_NAME = ""  

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com/'  
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)


bot = Bot(TOKEN)
dp = Dispatcher(bot)


admins = ['487656986', '766545273']
users = []


def autor(chatid):
    strid = str(chatid)
    for item in admins:
        if item == strid:
            return True
    return False


def user(chatid):
    strid = str(chatid)
    for item in users:
        if item == strid:
            return True
    return False


@dp.message_handler(commands=['user'])
async def user_count(message: types.Message):
	if autor(message.chat.id):
		await message.reply(len(users))
		try:
			for x in users:
				await message.answer(x)
		except:
			pass


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	if user(message.chat.id):
		await message.reply('Привет, отправь сообщение и оно опубликуется в WIUT CONFESSION.')
	else:
		await message.reply('Привет, отправь сообщение и оно опубликуется в WIUT CONFESSION.')
		users.append(message.chat.id)


@dp.message_handler(content_types=["text", "photo", "audio"])
@dp.message_handler(chat_type=ChatType.PRIVATE)
async def send_welcome(message: types.Message):
	if autor(message.chat.id):
		await message.answer(message.content_type)


	else:
		if message.text:
			await message.reply(f'*{message.from_user.first_name}*, сообщение (* {message.text} *) передано на обработку.', parse_mode="Markdown")

			for x in admins:
				text = f'{message.from_user.first_name}\n\
						@{str(message.from_user.username)}\n\
						{message.from_user.id}\n\n\
						{message.text}'
				try:
					await bot.send_message(x, text)
				except Exception as e:
					pass
		elif message.photo:
			msgcap = f'{message.from_user.first_name}\n\
					@{message.from_user.username}\n\
					{message.from_user.id}\n\n\
					{message.caption}'
			answer = f'*{message.from_user.first_name}*, фотография передана на обработку.'
			await bot.send_photo(message.chat.id, message.photo[-1].file_id, answer, parse_mode='Markdown')
			for x in admins:
				try:
					await bot.send_photo(x, message.photo[-1].file_id, msgcap)
				except Exception as e:
					pass


		elif message.audio:
			msgcap = f'{message.from_user.first_name}\n\
					@{message.from_user.username}\n\
					{message.from_user.id}\n\n\
					{message.caption}'
			answer = f'*{message.from_user.first_name}*, трек передан на обработку.'
			await bot.send_audio(message.chat.id, message.audio.file_id, answer, parse_mode='Markdown')
			for x in admins:
				try:
					await bot.send_audio(x, message.audio.file_id, msgcap)
				except Exception as e:
					pass


async def on_startup(app):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=os.getenv('PORT'))