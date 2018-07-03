import telebot
import os
from flask import Flask, request
import psycopg2
from telebot import types

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


@bot.message_handler(commands=['work'])
def start(message):
	userid = message.from_user.id
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute(f"UPDATE users SET coin = coin + 1 WHERE user_id={userid}")
	conn.commit()
	cursor.execute(f"select coin from users where user_id={userid}")
	results = cursor.fetchall()
	conn.close()
	bot.send_message(message.chat.id, results)


@bot.message_handler(commands=['new'])
def start(message):
	userid = message.from_user.id
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute(f"insert into users (user_id,coin) values({userid},'10')")
	conn.commit()
	conn.close()
	bot.reply_to(message, 'pong, ' + message.from_user.first_name)

@bot.message_handler(commands=['work2'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    work_button = types.InlineKeyboardButton(text="Перейти на Яндекс", callback_data="test")
    keyboard.add(work_button)
    bot.send_message(message.chat.id, "Работать", reply_markup=keyboard)	
	
	
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == "test":
			userid = call.message.from_user.id
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor = conn.cursor()
			cursor.execute(f"UPDATE users SET coin = coin + 1 WHERE user_id={userid}")
			conn.commit()
			cursor.execute(f"select coin from users where user_id={userid}")
			results = cursor.fetchall()
			conn.close()
			print (results)
			bot.send_message(call.message.chat.id, results)
			str = "Перейти на" + results
			bot.send_message(call.message.chat.id, str)
			keyboard2 = types.InlineKeyboardMarkup()
			work_button = types.InlineKeyboardButton(text=str, callback_data="test")
			keyboard2.add(work_button)			
			bot.edit_message_text(chat_id=call.message.chat.id,  message_id=call.message.message_id, text=str, reply_markup=keyboard2)


	

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