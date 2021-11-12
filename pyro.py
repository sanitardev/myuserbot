from pyrogram import Client, filters
import time as t
from datetime import datetime, timedelta
from pyowm import OWM
import random
import pytz
import sqlite3
from PIL import Image, ImageFilter
import tgcrypto

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

			


@app.on_message(filters.me & filters.command(["spam"], prefixes="."))
def spam(client, message):
	text = message.text.split()
	for spam in range(int(text[2])):
		app.send_message(message.chat.id, text[1])

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
	app.send_message(message.chat.id, 'Мои команды:\n.vzlom - взламывает жопу человека (реплай)\n.time - время в мск\n.weather (Город) - показывет какая сейчас погода в городе\n.random (Первое число) (Второе число) - выбирает случайное число в диапозоне двух чисел, также работает с одним числом\n.shakal (фото) - шакалит картинку\n.blur (фото) - блюрит картинку\n.pidoras - ищет пидораса \n.dolbaeb - ищет долбаеба\n.click - кликер')


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
	app.download_media(message.photo, file_name=path, block=True)
	original = Image.open("downloads/shakal.png")
	original.thumbnail(size)
	original.save("saved/shakal.png")
	original.show()
	app.send_photo(message.chat.id, "saved/shakal.png", caption="Вот твое фото:", reply_to_message_id=message.message_id)

@app.on_message(filters.command(["blur"], prefixes="."))
def blur(client, message):
	path = "shakal.png"
	app.download_media(message.photo, file_name=path, block=True)
	original = Image.open("downloads/shakal.png")
	blur = original.filter(ImageFilter.GaussianBlur(5))

	blur.save("saved/shakal.png")
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





app.run()