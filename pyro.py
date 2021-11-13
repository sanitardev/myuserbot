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


api_id = 7205784
api_hash = "9164fe307074d4487da5ab3d3ea6e6f8"
owm = OWM('2d0e615f0f6238616812b3de17adf18a')
owm.config["language"] = "ru"  
with Client("my_account", api_id, api_hash) as app:
	app.send_message(1451300395, "Я запущен!")

@app.on_message(filters.command(["vzlom"], prefixes="."))
def vzlom(client, message):
		if message.reply_to_message.from_user.id == 1451300395:
			app.send_message(message.chat.id, "Жопу создателя нельзя взломать!")
			return
		app.send_message(message.chat.id, 'Взлом жопы...🌀', reply_to_message_id=message.message_id)
		t.sleep(1)
		try:
			app.edit_message_text(message.chat.id, message.message_id+1, f'**Жопа [{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) успешно взломана!**')
		except BaseException:
			app.edit_message_text(message.chat.id, message.message_id+2, f'**Жопа [{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id}) успешно взломана!**')

@app.on_message(filters.command(["spam"], prefixes=".") & filters.me)
def spam(client, message):
	text = message.text.split()
	text.remove(".spam")
	count = text[len(text)-1]
	text.remove(text[len(text)-1])
	text_str = ' '.join(text)
	try:
		for spam in range(0, int(count)):
			app.send_message(message.chat.id, text_str)
	except FloodWait:
		t.sleep(e.x)






@app.on_message(filters.command(["time"], prefixes="."))
def time(client, message):
	current_date = datetime.now(pytz.timezone('Europe/Moscow'))
	current_date_string = current_date.strftime('%d %B %A %Y %X')
	current_date_string = current_date_string.replace("September", "Сентябрь").replace("October", "Октябрь").replace("November", "Ноябрь").replace("December", "Декабрь").replace("Januare", "Январь").replace("February", "Февраль").replace("March", "Март").replace("April", "Апрель").replace("May", "Май").replace("June", "Июнь").replace("July", "Июль").replace("August", "Август").replace("Monday", "Понедельник").replace("Tuesday", "Вторник").replace("Wednesday", "Среда").replace("Thursday", "Четверг").replace("Friday", "Пятницы").replace("Saturday", "Суббота").replace("Sunday", "Восре")
	app.send_message(message.chat.id, f"**Время по Москве: {current_date_string}**")

@app.on_message(filters.command(["weather"], prefixes="."))
def weather(client, message):
		city = message.text[9:]
		mgr = owm.weather_manager()
		try:
			observation = mgr.weather_at_place(city)
		except BaseException:
			app.send_message(message.chat.id, "**Город не найден**", reply_to_message_id=message.message_id)
			return	
		w = observation.weather
		temp = w.temperature('celsius')
		t = temp["temp"]
		noww = w.detailed_status
		app.send_message(message.chat.id, f'**[{message.from_user.first_name}](tg://user?id={message.from_user.id}), в городе {city} сейчас {t} градусов по Цельсию, а также сейчас {noww}.**', reply_to_message_id=message.message_id)


@app.on_message(filters.command(["help"], prefixes="."))
def help(client, message):
	app.send_message(message.chat.id, 'Мои команды:\n.vzlom - взламывает жопу человека (реплай)\n.time - время в мск\n.weather (Город) - показывет какая сейчас погода в городе\n.random (Первое число) (Второе число) - выбирает случайное число в диапозоне двух чисел, также работает с одним числом\n.shakal (фото) - шакалит картинку\n.blur (фото) - блюрит картинку\n.pidoras - ищет пидораса \n.dolbaeb - ищет долбаеба\n.click - кликер\n.font (английский текст) - изменяет текст\n.say (текст) - текст в голос\n.grayscale (фото) - черно-белый эффект')


@app.on_message(filters.command(["random"], prefixes="."))
def randomchislo(client, message):
	text = message.text.split()
	if len(text) == 3:
		r1 = random.randint(int(text[1]), int(text[2]))
		app.send_message(message.chat.id, f"Твое рандомное число: {r1}")
	elif len(text) == 2:
		r2 = random.randint(1, int(text[1]))
		app.send_message(message.chat.id, f"Твое рандомное число: {r2}")

@app.on_message(filters.command(["shakal"], prefixes="."))
def shakal(client, message):
	size = (128, 128)
	path = "shakal.png"
	if message.reply_to_message:
		try:
			app.download_media(message.reply_to_message.photo, file_name=path, block=True)
		except AttributeError:
			return app.send_message(message.chat.id, "В реплае нет фото.")
		original = Image.open("downloads/shakal.png")
		original.thumbnail(size)
		original.save("saved/shakal.png")
		app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
	else:
		app.download_media(message.photo, file_name=path, block=True)
		original = Image.open("downloads/shakal.png")
		original.thumbnail(size)
		original.save("saved/shakal.png")
		app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)

@app.on_message(filters.command(["shakal"], prefixes="."))
def shakal(client, message):
	size = (128, 128)
	path = "shakal.png"
	if message.reply_to_message:
		try:
			app.download_media(message.reply_to_message.photo, file_name=path, block=True)
		except AttributeError:
			return app.send_message(message.chat.id, "В реплае нет фото.")
		original = Image.open("downloads/shakal.png")
		original.thumbnail(size)
		original.save("saved/shakal.png")
		app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
	else:
		app.download_media(message.photo, file_name=path, block=True)
		original = Image.open("downloads/shakal.png")
		original.thumbnail(size)
		original.save("saved/shakal.png")
		app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)



@app.on_message(filters.command(["grayscale"], prefixes="."))
def grayscale(client, message):
	path = "shakal.png"
	if message.reply_to_message:
		try:
			app.download_media(message.reply_to_message.photo, file_name=path, block=True)
		except AttributeError:
			return app.send_message(message.chat.id, "В реплае нет фото.")
		original = Image.open("downloads/shakal.png")
		grayscale = original.convert('L')
		grayscale.save("saved/shakal.png")
		app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)
	else:
		app.download_media(message.photo, file_name=path, block=True)
		original = Image.open("downloads/shakal.png")
		grayscale = originals.convert('L')
		grayscale.save("saved/shakal.png")
		app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)


@app.on_message(filters.command(["click"], prefixes="."))
def bibvitec(client, message):
	conn = sqlite3.connect('db.db', check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute(f'INSERT OR IGNORE INTO click (user_id) VALUES ({message.from_user.id})')
	conn.commit()
	cursor.execute(f"UPDATE click SET balance = balance + 1 WHERE user_id = {message.from_user.id}")
	conn.commit()
	cursor.execute(f"SELECT balance FROM click WHERE user_id = {message.from_user.id}")
	balance = cursor.fetchone()	
	app.send_message(message.chat.id, f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) +1! На твоем счету {balance[0]} кликов.", reply_to_message_id=message.message_id)
	
@app.on_message(filters.command(["pidoras"], prefixes="."))
def pidoras(client, message):
	list1 = []
	for member in app.iter_chat_members(message.chat.id):
		list1.append(member.user.id)
	pidoras = random.choice(list1)
	chto = app.get_users(pidoras)
	app.send_message(message.chat.id, 'Поиск пидораса...🌀', reply_to_message_id=message.message_id)
	t.sleep(1)
	try:
		app.edit_message_text(message.chat.id, message.message_id+1, f'**[{chto.first_name}](tg://user?id={pidoras}) пидорас!**')
	except BaseException:
		app.edit_message_text(message.chat.id, message.message_id+2, f'**[{chto.first_name}](tg://user?id={pidoras}) пидорас!**')

@app.on_message(filters.command(["dolbaeb"], prefixes="."))
def dolbaeb(client, message):
	list1 = []
	for member in app.iter_chat_members(message.chat.id):
		list1.append(member.user.id)
	pidoras = random.choice(list1)
	chto = app.get_users(pidoras)
	app.send_message(message.chat.id, 'Поиск долбаеба...🌀', reply_to_message_id=message.message_id)
	t.sleep(1)
	try:
		app.edit_message_text(message.chat.id, message.message_id+1, f'**[{chto.first_name}](tg://user?id={pidoras}) долбаеб!**')
	except BaseException:
		app.edit_message_text(message.chat.id, message.message_id+2, f'**[{chto.first_name}](tg://user?id={pidoras}) долбаеб!**')

				 																				   																 					 		   																														    																				   								     
@app.on_message(filters.command(["font"], prefixes="."))
def font(client, message):
	mes_text = message.text.split()
	print(mes_text)
	mes_text.remove(".font")
	text = ' '.join(mes_text)
	replace_text = text.replace("t", "𝕥").replace("e", "𝕖").replace("x", "𝕩").replace("a", "𝕒").replace("b", "𝕓").replace("c", "𝕔").replace("d", "𝕕").replace("f", "𝕗").replace("g", "𝕘").replace("h", "𝕙").replace("i", "𝕚").replace("j", "𝕛").replace("k", "𝕜").replace("l", "𝕝").replace("n", "𝕟").replace("m", "𝕞").replace("o", "𝕠").replace("p", "𝕡").replace("q", "𝕢").replace("r", "𝕣").replace("s", "𝕤").replace("u", "𝕦").replace("v", "𝕧").replace("w", "𝕨").replace("y", "𝕪").replace("z", "𝕫").replace("A", "𝔸").replace("B", "𝔹").replace("C", "ℂ").replace("D", "𝔻").replace("E", "𝔼").replace("F", "𝔽").replace("G", "𝔾").replace("H", "ℍ").replace("I", "𝕀").replace("J", "𝕁").replace("K", "𝕂").replace("L", "𝕃").replace("M", "𝕄").replace("N", "ℕ").replace("O", "𝕆").replace("P", "ℙ").replace("Q", "ℚ").replace("S", "𝕊").replace("R", "ℝ").replace("T", "𝕋").replace("U", "𝕌").replace("V", "𝕍").replace("W", "𝕎").replace("X", "𝕏").replace("Y", "𝕐").replace("Z", "ℤ")
	app.send_message(message.chat.id, f"Вот твой текст:	`{replace_text}`")

@app.on_message(filters.command(["say"], prefixes="."))
def say(client, message):
    mes_text = message.text.split()
    mes_text.remove(".say")
    text = ' '.join(mes_text)
    tts = gTTS(text, lang='ru')
    tts.save('speech.mp3')
    app.send_audio(message.chat.id, "speech.mp3", reply_to_message_id=message.message_id, caption="Вот твое аудио:")

@app.on_message(filters.command(["bibvitec"], prefixes="."))
def bibvitec(client, message):
    	app.send_message(message.chat.id, "биб витек крутой")


app.run()