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
import random


DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Helo, ' + message.from_user.first_name)
	
@bot.message_handler(commands=['help'])
def start(message):
    bot.reply_to(message, """
	/me
	/build
	/work
	\new
	/research
	""" + message.from_user.first_name)

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
	jon["build"]["n"]=0
	jon["build"]["workers"]=0
	jon["build"]["warrior"]=0
	jon=json.dumps(jon)
	cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
	conn.commit()
	conn.close()

@bot.message_handler(commands=['work'])
def default_test(message):
	keyboard = types.InlineKeyboardMarkup()
	work_button = types.InlineKeyboardButton(text="Кликай, чтобы заработать!", callback_data="work")
	exped_button = types.InlineKeyboardButton(text="Отправить рабочих в експедицию 5 рабочих", callback_data="exped")
	keyboard.add(work_button)
	keyboard.add(exped_button)
	bot.send_message(message.chat.id, "Работать", reply_markup=keyboard)	
	
@bot.message_handler(commands=['build'])
def default_test(message):
	userid = message.from_user.id
	keyboard = types.InlineKeyboardMarkup()
	n_count =  f_builds ('?',userid,"n",0)
	n_cost = n_count*n_count
	work_button = types.InlineKeyboardButton(text=(f"Строить N\n за ${n_cost}"), callback_data="N")
	workers_button = types.InlineKeyboardButton(text=(f"Строить Рабочих\n за $10"), callback_data="workers")
	warrior_button = types.InlineKeyboardButton(text=(f"Строить Воинов\n за $50"), callback_data="warrior")
	keyboard.add(work_button)
	keyboard.add(workers_button)
	keyboard.add(warrior_button)
	bot.send_message(message.chat.id, "Построить чет?", reply_markup=keyboard)	

@bot.message_handler(commands=['me'])
def default_test(message):
	userid = message.from_user.id
	coin =  f_coin ('?',userid, 0)
	n_count =  f_builds ('?',userid,"n",0)
	workers_count =  f_builds ('?',userid, "workers", 0)
	warrior_count =  f_builds ('?',userid, "warrior", 0)
	coin =  f_coin ('?',userid, 0)
	bot.send_message(message.chat.id, (f"Монет: {coin} \n\n Постройки: \n N = {n_count}\n\n Постройки: \n workers_count = {workers_count} \n warrior_count = {warrior_count}"))

@bot.message_handler(commands=['research'])
def default_test(message):
	userid = message.from_user.id
	bot.send_message(message.chat.id, (f"◽️◽️◽️◽️◽️◽️◽️◽️◽️"))
	msgid=message.message_id+1
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◽️◽️◽️◽️◽️◽️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◽️◽️◽️◽️◽️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◽️◽️◽️◽️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◽️◽️◽️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◽️◽️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◽️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◽️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◾️◽️"))
	time.sleep(1) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◾️◾️"))



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		if call.data == "work":
			userid = call.from_user.id
			f_coin ('+',userid, 1)
			coin =  f_coin ('?',userid, 0)
			str2 = (f"$ = {coin}")
			keyboard2 = types.InlineKeyboardMarkup()
			work_button = types.InlineKeyboardButton(text=str2, callback_data="work")
			keyboard2.add(work_button)
			bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=keyboard2)
		if call.data == "N":
			userid = call.from_user.id
			coin =  f_coin ('?',userid, 0)
			n_count =  f_builds ('?',userid, "n", 0)
			n_cost=n_count*n_count
			if int(coin) >= n_cost:
				f_coin ('+',userid, -n_cost)
				n_count =  f_builds ('+',userid,"n", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="N")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} N \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")
				
		if call.data == "workers":
			userid = call.from_user.id
			coin =  f_coin ('?',userid, 0)
			n_count =  f_builds ('?',userid, "workers", 0)
			n_cost=10
			if int(coin) >= n_cost:
				f_coin ('+',userid, -n_cost)
				n_count =  f_builds ('+',userid,"workers", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="workers")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} рабочих \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")
				
		if call.data == "warrior":
			userid = call.from_user.id
			coin =  f_coin ('?',userid, 0)
			n_count =  f_builds ('?',userid, "warrior", 0)
			work_count =  f_builds ('?',userid, "workers", 0)
			n_cost=50
			if int(coin) >= n_cost and work_count >= 1 :
				f_coin ('+',userid, -n_cost)
				f_builds ('+',userid,"workers", -1)
				n_count =  f_builds ('+',userid,"warrior", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="warrior")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} воинов \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")

				

			
		if call.data == "exped":
			userid = call.from_user.id
			workers_count=f_builds ('?',userid,"workers", 0)
			if (workers_count >= 5):
				f_builds ('+',userid,"workers", -5)
				bot.send_message(call.message.chat.id, (f"Рабочие вернутся через 15 секунд"))
				time.sleep(15) 
				f_builds ('+',userid,"workers", +5)
				conn = psycopg2.connect(DATABASE_URL, sslmode='require')
				cursor2 = conn.cursor()
				new_coin = abs(round(round(random.normalvariate(12, 12),-1)))
				cursor2.execute(f"UPDATE users SET coin = coin + {new_coin} WHERE user_id={userid}")
				conn.commit()
				conn.close()
				bot.send_message(call.message.chat.id, (f"Рабочие нашли ${new_coin}"))
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")
		
		
				

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