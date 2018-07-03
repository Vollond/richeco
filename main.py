import telebot
import os
from flask import Flask, request
import psycopg2
from telebot import types
import re


DATABASE_URL = os.environ['DATABASE_URL']



bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')

server = Flask(__name__)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Helo, ' + message.from_user.first_name)

@bot.message_handler(commands=['ping'])
def start(message):
	bot.send_message(message.chat.id, 'pong, ' + message.from_user.first_name)
	bot.send_message(message.chat.id, 'pong, ' + message.from_user.id)


@bot.message_handler(commands=['new'])
def start(message):
	userid = message.from_user.id
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute(f"insert into users (user_id,coin) values({userid},'10')")
	conn.commit()
	conn.close()
	bot.reply_to(message, 'pong, ' + message.from_user.first_name)

@bot.message_handler(commands=['work'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    work_button = types.InlineKeyboardButton(text="Кликай, чтобы заработать!", callback_data="test")
    keyboard.add(work_button)
    bot.send_message(message.chat.id, "Работать", reply_markup=keyboard)	
	
@bot.message_handler(commands=['build'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    work_button = types.InlineKeyboardButton(text="Строим!", callback_data="N")
    keyboard.add(work_button)
    bot.send_message(message.chat.id, "Построить N за 10 монет", reply_markup=keyboard)	

	
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == "test":
			userid = call.from_user.id
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor2 = conn.cursor()
			cursor2.execute(f"UPDATE users SET coin = coin + 1 WHERE user_id={userid}")
			cursor2.execute(f"select coin from users where user_id={userid}")
			results2 = cursor2.fetchall()
			results2 = ''.join(str(e) for e in results2)
			results2 = re.findall(r'\d*\d', (str(results2)))
			results2=results2[0]
			conn.commit()
			conn.close()
			str2 = (f"$ = {results2}")
			keyboard2 = types.InlineKeyboardMarkup()
			work_button = types.InlineKeyboardButton(text=str2, callback_data="test")
			keyboard2.add(work_button)
			bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=keyboard2)
		if call.data == "N":
			userid = call.from_user.id
			from collections import defaultdict
			_default_data = lambda: defaultdict(_default_data)
			jon = _default_data()
			import json
			jon["build"]["n"]=1
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor2 = conn.cursor()
			jon2=json.dumps(jon)
			jon3 = json.loads(jon2)

			cursor2.execute(f"UPDATE users SET date = {jon3} WHERE user_id={userid}")
			
			conn.commit()
			conn.close()

	

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://richeco.herokuapp.com/bot")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 8443))
server = Flask(__name__)