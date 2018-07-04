import telebot
import os
from flask import Flask, request
import psycopg2
from telebot import types
import re
import json
from collections import defaultdict
_default_data = lambda: defaultdict(_default_data)
import time
from funs import f_coin
from funs import f_builds

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
	cursor.execute(f"delete from users where user_id={userid}")
	cursor.execute(f"insert into users (user_id,coin) values({userid}, 10)")
	jon = _default_data()
	jon["build"]["n"]=1
	jon=json.dumps(jon)
	cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
	conn.commit()
	conn.close()

@bot.message_handler(commands=['work'])
def default_test(message):
	keyboard = types.InlineKeyboardMarkup()
	work_button = types.InlineKeyboardButton(text="Кликай, чтобы заработать!", callback_data="work")
	exped_button = types.InlineKeyboardButton(text="Отправить рабочих в експедицию", callback_data="exped")
	keyboard.add(work_button)
	keyboard.add(exped_button)
	bot.send_message(message.chat.id, "Работать", reply_markup=keyboard)	
	
@bot.message_handler(commands=['build'])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    work_button = types.InlineKeyboardButton(text="Строим!", callback_data="N")
    keyboard.add(work_button)
    bot.send_message(message.chat.id, "Построить N?", reply_markup=keyboard)	

@bot.message_handler(commands=['me'])
def default_test(message):
	userid = message.from_user.id
	coin =  f_coin ('?',userid)
	n_count =  f_builds ('?',userid)
	bot.send_message(message.chat.id, (f"Монет: {coin} \n\n Постройки: \n N = {n_count}"))



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == "work":
			userid = call.from_user.id
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor2 = conn.cursor()
			cursor2.execute(f"UPDATE users SET coin = coin + 1 WHERE user_id={userid}")
			cursor2.execute(f"select coin from users where user_id={userid}")
			coin = cursor2.fetchall()
			coin = coin[0][0]
			conn.commit()
			conn.close()
			str2 = (f"$ = {coin}")
			keyboard2 = types.InlineKeyboardMarkup()
			work_button = types.InlineKeyboardButton(text=str2, callback_data="work")
			keyboard2.add(work_button)
			bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=keyboard2)
		if call.data == "N":
			userid = call.from_user.id
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor = conn.cursor()
			cursor.execute(f"select coin from users where user_id={userid}")
			coin = cursor.fetchall()
			coin=coin[0][0]
			jon = _default_data()
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor2 = conn.cursor()
			cursor2.execute(f"select date from users where user_id={userid}")
			jonew = cursor2.fetchall()
			jonew = jonew[0][0]
			jonew["build"]["n"] = jonew["build"]["n"] +1
			n_count = jonew["build"]["n"]
			jon=json.dumps(jonew)
			n_cost=n_count*n_count
			if int(coin) >= n_cost:
				cursor2.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
				cursor2.execute(f"UPDATE users SET coin = coin - {n_cost} WHERE user_id={userid}")
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="N")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Строим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")

			conn.commit()
			conn.close()
			
		if call.data == "exped":
			bot.send_message(call.message.chat.id, (f"Рабочие вернутся через 15 секунд"))
			time.sleep(15) 
			userid = call.from_user.id
			conn = psycopg2.connect(DATABASE_URL, sslmode='require')
			cursor2 = conn.cursor()
			new_coin = 10
			cursor2.execute(f"UPDATE users SET coin = coin + {new_coin} WHERE user_id={userid}")
			conn.commit()
			conn.close()
			bot.send_message(call.message.chat.id, (f"Рабочие нашли ${new_coin}"))


		
		
	

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