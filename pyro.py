from pyrogram import Client, filters
from pyrogram.errors import FloodWait, SlowmodeWait
import time as t
from datetime import datetime, timedelta
from pyowm import OWM
import random
import pytz
import sqlite3
from PIL import Image, ImageFilter
import tgcrypto
from gtts import gTTS
from pyrogram.raw import functions
from config import api_id, api_hash, owmtoken
import asyncio
import os
import requests
from ImageParser import YandexImage

app = Client("my_account", api_id, api_hash)

owm = OWM(owmtoken)
owm.config["language"] = "ru"  

@app.on_message(filters.command(["vzlom"], prefixes="."))
async def vzlom(client, message):
		if not message.reply_to_message:
			await app.send_message(message.chat.id, 'Это не реплай!', reply_to_message_id=message.message_id)
			return
		if message.reply_to_message.from_user.id == 1451300395:
			await app.send_message(message.chat.id, "Жопу создателя нельзя взломать!", reply_to_message_id=message.message_id)
			return
		vzlom = await app.send_message(message.chat.id, 'Взлом жопы...🌀', reply_to_message_id=message.message_id)
		await asyncio.sleep(1)
		await app.edit_message_text(message.chat.id, vzlom.message_id, f'**Жопа [{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) успешно взломана!**')


@app.on_message(filters.command(["spam"], prefixes=".") & filters.me)
async def spam(client, message):
	text = message.text.split()
	text.remove(".spam")
	count = text[len(text)-1]
	text.remove(text[len(text)-1])
	text_str = ' '.join(text)
	try:
		for spam in range(0, int(count)):
			await app.send_message(message.chat.id, text_str)
	except FloodWait:
		await asyncio.sleep(e.x)

@app.on_message(filters.command(["time"], prefixes="."))
async def time(client, message):
	current_date = datetime.now(pytz.timezone('Europe/Moscow'))
	current_date_string = current_date.strftime('%x %X, %A')
	current_date_string = current_date_string.replace("September", "Сентябрь").replace("October", "Октябрь").replace("November", "Ноябрь").replace("December", "Декабрь").replace("Januare", "Январь").replace("February", "Февраль").replace("March", "Март").replace("April", "Апрель").replace("May", "Май").replace("June", "Июнь").replace("July", "Июль").replace("August", "Август").replace("Monday", "Понедельник").replace("Tuesday", "Вторник").replace("Wednesday", "Среда").replace("Thursday", "Четверг").replace("Friday", "Пятница").replace("Saturday", "Суббота").replace("Sunday", "Воскресенье")
	await app.send_message(message.chat.id, f"**Время по Москве: {current_date_string}**", reply_to_message_id=message.message_id)

@app.on_message(filters.command(["weather"], prefixes="."))
async def weather(client, message):
		city = message.text[9:]
		mgr = owm.weather_manager()
		try:
			observation = mgr.weather_at_place(city)
		except BaseException:
			await app.send_message(message.chat.id, "**Город не найден**", reply_to_message_id=message.message_id)
			return	
		w = observation.weather
		temp = w.temperature('celsius')
		t = temp["temp"]
		noww = w.detailed_status
		await app.send_message(message.chat.id, f'**[{message.from_user.first_name}](tg://user?id={message.from_user.id}), в городе {city} сейчас: {int(t)}°, {noww}.**', reply_to_message_id=message.message_id)

@app.on_message(filters.command(["help"], prefixes="."))
async def help(client, message):
	conn = sqlite3.connect('db.db', check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("SELECT COUNT(*) FROM stik")
	count = cursor.fetchone()
	await app.send_message(message.chat.id, f'**Мои команды:\n.vzlom - взламывает жопу человека (реплай)\n.time - время в мск\n.weather (Город) - показывет какая сейчас погода в городе\n.random (Первое число) (Второе число) - выбирает случайное число в диапозоне двух чисел, также работает с одним числом\n.shakal (фото или реплай на фото) - шакалит картинку\n.blur (фото или реплай на фото) - блюрит картинку\n.pidoras - ищет пидораса \n.dolbaeb - ищет долбаеба\n.click - кликер\n.font (английский текст) - изменяет текст\n.say (текст) - текст в голос\n.grayscale (фото или реплай на фото) - черно-белый эффект\n.stickers - отравляет рандомный стикер из базы данных(в базе данных {count[0]} стикеров).\n.photo (текст) - ищет фото по запросу.**', reply_to_message_id=message.message_id)

@app.on_message(filters.command(["random"], prefixes="."))
async def randomchislo(client, message):
	text = message.text.split()
	if len(text) == 3:
		r1 = random.randint(int(text[1]), int(text[2]))
		await app.send_message(message.chat.id, f"Твое рандомное число: {r1}")
	elif len(text) == 2:
		r2 = random.randint(1, int(text[1]))
		await app.send_message(message.chat.id, f"Твое рандомное число: {r2}")
	else:
		await app.send_message(message.chat.id, "Слишком много чисел или нет чисел!", reply_to_message_id=message.message_id)


@app.on_message(filters.command(["shakal"], prefixes="."))
async def shakal(client, message):
	size = (128, 128)
	path = "shakal.png"
	if message.reply_to_message:
		try:
			await app.download_media(message.reply_to_message.photo, file_name=path, block=True)
		except AttributeError:
			return await app.send_message(message.chat.id, "В реплае нет фото.")
		original = Image.open("downloads/shakal.png")
		original.thumbnail(size)
		original.save("saved/shakal.png")
		await app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
		os.remove("downloads/shakal.png")
		os.remove("saved/shakal.png")		
	else:
		try:
			await app.download_media(message.photo, file_name=path, block=True)
		except AttributeError:
			return await app.send_message(message.chat.id, "Прикрепи фото!")
		original = Image.open("downloads/shakal.png")
		original.thumbnail(size)
		original.save("saved/shakal.png")
		await app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
		os.remove("downloads/shakal.png")
		os.remove("saved/shakal.png")

@app.on_message(filters.command(["blur"], prefixes="."))
async def blur(client, message):
	path = "shakal.png"
	if message.reply_to_message:
		try:
			await app.download_media(message.reply_to_message.photo, file_name=path, block=True)
		except AttributeError:
			return await app.send_message(message.chat.id, "В реплае нет фото.")
		original = Image.open("downloads/shakal.png")
		blur = original.filter(ImageFilter.GaussianBlur(5))
		blur.save("saved/shakal.png")
		await app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
		os.remove("downloads/shakal.png")
		os.remove("saved/shakal.png")		
	else:
		try:
			await app.download_media(message.photo, file_name=path, block=True)
		except AttributeError:
			return await app.send_message(message.chat.id, "Прикрепи фото!")
		original = Image.open("downloads/shakal.png")
		blur = original.filter(ImageFilter.GaussianBlur(5))
		blur.save("saved/shakal.png")
		await app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
		os.remove("downloads/shakal.png")
		os.remove("saved/shakal.png")

@app.on_message(filters.command(["grayscale"], prefixes="."))
async def grayscale(client, message):
	path = "shakal.png"
	if message.reply_to_message:
		try:
			await app.download_media(message.reply_to_message.photo, file_name=path, block=True)
		except AttributeError:
			return await app.send_message(message.chat.id, "В реплае нет фото.")
		original = Image.open("downloads/shakal.png")
		grayscale = original.convert('L')
		grayscale.save("saved/shakal.png")
		await app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
		os.remove("downloads/shakal.png")
		os.remove("saved/shakal.png")
	else:
		try:
			await app.download_media(message.photo, file_name=path, block=True)
		except AttributeError:
			return await app.send_message(message.chat.id, "Прикрепи фото!")
		original = Image.open("downloads/shakal.png")
		grayscale = original.convert('L')
		grayscale.save("saved/shakal.png")
		await app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
		os.remove("downloads/shakal.png")
		os.remove("saved/shakal.png")

@app.on_message(filters.command(["click"], prefixes="."))
async def bibvitec(client, message):
	conn = sqlite3.connect('db.db', check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute(f'INSERT OR IGNORE INTO click (user_id) VALUES ({message.from_user.id})')
	conn.commit()
	cursor.execute(f"UPDATE click SET balance = balance + 1 WHERE user_id = {message.from_user.id}")
	conn.commit()
	cursor.execute(f"SELECT balance FROM click WHERE user_id = {message.from_user.id}")
	balance = cursor.fetchone()	
	await app.send_message(message.chat.id, f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) +1! На твоем счету {balance[0]} кликов.", reply_to_message_id=message.message_id)
	
@app.on_message(filters.command(["pidoras"], prefixes="."))
async def pidoras(client, message):
	list1 = []
	async for member in app.iter_chat_members(message.chat.id):
		list1.append(member.user.id)
	pidoras_id = random.choice(list1)
	pidoras = await app.get_users(pidoras_id)
	pidoras_name = pidoras.first_name
	pidor = await app.send_message(message.chat.id, 'Поиск пидораса...🌀', reply_to_message_id=message.message_id)
	await asyncio.sleep(1)
	await app.edit_message_text(message.chat.id, pidor.message_id, f'**[{pidoras_name}](tg://user?id={pidoras_id}) пидорас!**')


@app.on_message(filters.command(["dolbaeb"], prefixes="."))
async def dolbaeb(client, message):
	list1 = []
	async for member in app.iter_chat_members(message.chat.id):
		list1.append(member.user.id)
	pidoras_id = random.choice(list1)
	pidoras = await app.get_users(pidoras_id)
	pidoras_name = pidoras.first_name
	dolb = await app.send_message(message.chat.id, 'Поиск долбаеба...🌀', reply_to_message_id=message.message_id)
	await asyncio.sleep(1)
	await app.edit_message_text(message.chat.id, dolb.message_id, f'**[{pidoras_name}](tg://user?id={pidoras_id}) долбаеб!**')
			 																				   																 					 		   																														    																				   								     
@app.on_message(filters.command(["font"], prefixes="."))
async def font(client, message):
	mes_text = message.text.split()
	mes_text.remove(".font")
	text = ' '.join(mes_text)
	if text == "":
		await app.send_message(message.chat.id, "Напиши текст(поддерживается только английский)!", reply_to_message_id=message.message_id)
		return
	replace_text = text.replace("t", "𝕥").replace("e", "𝕖").replace("x", "𝕩").replace("a", "𝕒").replace("b", "𝕓").replace("c", "𝕔").replace("d", "𝕕").replace("f", "𝕗").replace("g", "𝕘").replace("h", "𝕙").replace("i", "𝕚").replace("j", "𝕛").replace("k", "𝕜").replace("l", "𝕝").replace("n", "𝕟").replace("m", "𝕞").replace("o", "𝕠").replace("p", "𝕡").replace("q", "𝕢").replace("r", "𝕣").replace("s", "𝕤").replace("u", "𝕦").replace("v", "𝕧").replace("w", "𝕨").replace("y", "𝕪").replace("z", "𝕫").replace("A", "𝔸").replace("B", "𝔹").replace("C", "ℂ").replace("D", "𝔻").replace("E", "𝔼").replace("F", "𝔽").replace("G", "𝔾").replace("H", "ℍ").replace("I", "𝕀").replace("J", "𝕁").replace("K", "𝕂").replace("L", "𝕃").replace("M", "𝕄").replace("N", "ℕ").replace("O", "𝕆").replace("P", "ℙ").replace("Q", "ℚ").replace("S", "𝕊").replace("R", "ℝ").replace("T", "𝕋").replace("U", "𝕌").replace("V", "𝕍").replace("W", "𝕎").replace("X", "𝕏").replace("Y", "𝕐").replace("Z", "ℤ")
	await app.send_message(message.chat.id, f"Вот твой текст:	`{replace_text}`")

@app.on_message(filters.command(["say"], prefixes="."))
async def say(client, message):
    mes_text = message.text.split()
    mes_text.remove(".say")
    text = ' '.join(mes_text)
    try:
    	tts = gTTS(text, lang='ru')
    except AssertionError:
    	await app.send_audio(message.chat.id, "Напиши текст для озучки!")
    tts.save('speech.mp3')
    await app.send_audio(message.chat.id, "speech.mp3", reply_to_message_id=message.message_id, caption="Вот твое аудио:")

@app.on_message(filters.command(["bibvitec"], prefixes="."))
async def bibvitec(client, message):
    	app.send_message(message.chat.id, "биб витек крутой")

@app.on_message(filters.command(["stickers"], prefixes="."))
async def stickers(client, message):
	conn = sqlite3.connect('db.db', check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute(f"SELECT stik_id FROM stik")	
	ids = cursor.fetchall()
	random_ids = random.choice(ids)
	await app.send_sticker(message.chat.id, random_ids[0], reply_to_message_id=message.message_id)

@app.on_message(filters.sticker)
async def stickers(client, message):
	conn = sqlite3.connect('db.db', check_same_thread=False)
	cursor = conn.cursor()
	stik = message.sticker
	idstik = stik.file_id
	cursor.execute(f'INSERT INTO stik (stik_id) VALUES (?)', (idstik,))
	conn.commit()

@app.on_message(filters.command(["photo"], prefixes="."))
async def photo(client, message):
	list1 = []
	parser = YandexImage()
	mes_text = message.text.split()
	mes_text.remove(".photo")
	text = ' '.join(mes_text)
	for item in parser.search(text):
		list1.append(item.url)
	
	try:
		randomurl = random.choice(list1)
	except IndexError:
		await app.send_message(message.chat.id, "Фото не найдено!")
		return
	print(randomurl)


app.run()