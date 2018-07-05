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
from battles import defens



DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Helo, ' + message.from_user.first_name)
	
@bot.message_handler(commands=['help'])
def start(message):
    bot.reply_to(message, """
	/menu
	""")
	
@bot.message_handler(commands=['menu'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row('work', 'exped')
	markup.row('me', 'build', 'research')
	bot.send_message(message.chat.id, "Choose:", reply_markup=markup)

	
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
	jon["build"]["exped"]=0
	jon["build"]["crystal"]=0
	jon=json.dumps(jon)
	cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
	conn.commit()
	conn.close()

@bot.message_handler(func=lambda mess: mess.text=='work' and mess.content_type=='text')
def default_test(message):
	keyboard = types.InlineKeyboardMarkup()
	work_button = types.InlineKeyboardButton(text="Кликай, чтобы заработать!", callback_data="work")
	exped_button = types.InlineKeyboardButton(text="Отправить 5 человек в шахту", callback_data="exped")
	keyboard.add(work_button)
	keyboard.add(exped_button)
	bot.send_message(message.chat.id, "Работать", reply_markup=keyboard)	
	
@bot.message_handler(func=lambda mess: mess.text=='exped' and mess.content_type=='text')
def default_test(message):
	keyboard = types.InlineKeyboardMarkup()
	forest_button = types.InlineKeyboardButton(text="Отправить 20 человек исследовать лес", callback_data="forest")
	unknown_place_button = types.InlineKeyboardButton(text="Отправить 50 человек исследовать черт знает что неподалеку", callback_data="unknown_place")
	keyboard.add(forest_button)
	keyboard.add(unknown_place_button)
	bot.send_message(message.chat.id, "Работать", reply_markup=keyboard)		

@bot.message_handler(func=lambda mess: mess.text=='build' and mess.content_type=='text')	
def default_test(message):
	userid = message.from_user.id
	keyboard = types.InlineKeyboardMarkup()
	n_count =  f_builds ('?',userid,"n",0)
	n_cost = n_count*n_count
	work_button = types.InlineKeyboardButton(text=(f"N-центр"), callback_data="N")
	workers_button = types.InlineKeyboardButton(text=(f"Рабочих"), callback_data="workers")
	warrior_button = types.InlineKeyboardButton(text=(f"Воинов"), callback_data="warrior")
	keyboard.add(work_button)
	keyboard.add(workers_button)
	keyboard.add(warrior_button)
	bot.send_message(message.chat.id, """
	Построить чет?
	Строить N-центр\n за ${n_cost}
	Строить Рабочих\n за $10
	Строить Воинов\n за $50
	""", reply_markup=keyboard)	

@bot.message_handler(func=lambda mess: mess.text=='me' and mess.content_type=='text')	
def default_test(message):
	userid = message.from_user.id
	coin =  f_coin ('?',userid, 0)
	n_count =  f_builds ('?',userid,"n",0)
	workers_count =  f_builds ('?',userid, "workers", 0)
	warrior_count =  f_builds ('?',userid, "warrior", 0)
	coin =  f_coin ('?',userid, 0)
	bot.send_message(message.chat.id, (f"Монет: {coin} \n\n Постройки: \n N-центры = {n_count}\n\n Постройки: \n workers_count = {workers_count} \n warrior_count = {warrior_count}"))

@bot.message_handler(func=lambda mess: mess.text=='research' and mess.content_type=='text')	
def default_test(message):
	userid = message.from_user.id
	bot.send_message(message.chat.id, (f"◽️◽️◽️◽️◽️◽️◽️◽️◽️"))
	msgid=message.message_id+1
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◽️◽️◽️◽️◽️◽️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◽️◽️◽️◽️◽️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◽️◽️◽️◽️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◽️◽️◽️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◽️◽️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◽️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◽️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◾️◽️"))
	time.sleep(10) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◾️◾️"))



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message:
		userid = call.from_user.id 
		if (f_coin('?',userid, 0)>40) and (random.randint(0,100)<3): #BATLLES
			bot.send_message(call.message.chat.id, (f"На вас напали"))
			batl_res, score = defens(userid, "rand")
			bot.send_message(message.chat.id, (f"{batl_res}"))	

			
		if call.data == "work":
			f_coin ('+',userid, 1)
			coin =  f_coin ('?',userid, 0)
			str2 = (f"$ = {coin}")
			keyboard2 = types.InlineKeyboardMarkup()
			work_button = types.InlineKeyboardButton(text=str2, callback_data="work")
			keyboard2.add(work_button)
			bot.edit_message_reply_markup(chat_id=call.message.chat.id,  message_id=call.message.message_id, reply_markup=keyboard2)
		if call.data == "N":
			coin =  f_coin ('?',userid, 0)
			n_count =  f_builds ('?',userid, "n", 0)
			n_cost=n_count*n_count
			if int(coin) >= n_cost:
				f_coin ('+',userid, - n_cost)
				n_count =  f_builds ('+',userid,"n", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="N")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} N-центров \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")
				
		if call.data == "workers":
			coin =  f_coin ('?',userid, 0)
			n_count =  f_builds ('?',userid, "workers", 0)
			n_cost=10
			if int(coin) >= n_cost:
				f_coin ('+',userid, - n_cost)
				n_count =  f_builds ('+',userid,"workers", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="workers")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} рабочих \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!\n /work")
				
		if call.data == "warrior":
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

				

			
		if call.data == "mine":
			workers_count=f_builds ('?',userid,"workers", 0)
			exped_count=f_builds ('?',userid,"exped", 0)	
			if (exped_count <1):
				if (workers_count >= 5):
					f_builds ('+',userid,"exped", +1)
					f_builds ('+',userid,"workers", -5)
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=(f"Рабочие скоро вернутся"))
					time.sleep(random.randint(15,50))
					f_builds ('+',userid,"workers", +5)
					f_builds ('+',userid,"exped", -1)
					new_coin = round((abs(round(random.normalvariate(12, 12),-1)))/2)
					f_coin('+',userid, new_coin)
					bot.send_message(call.message.chat.id, (f"Рабочие нашли ${new_coin}"))
				else:
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает людей!\n /work")
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="У вас уже отправленна експедиция!\n /work")
		
		if call.data == "forest":
			workers_count=f_builds ('?',userid,"workers", 0)
			exped_count=f_builds ('?',userid,"exped", 0)	
			if (exped_count <1):
				if (workers_count >= 20):
					f_builds ('+',userid,"exped", +1)
					f_builds ('+',userid,"workers", -20)
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=(f"Рабочие скоро вернутся"))
					quality = random.randint(1,5)
					time.sleep(random.randint(30,80)*quality)
					sid = random.randint(1,4000)*quality/3
					if(sid>4000):
						f_builds ('+',userid,"workers", +20)			
						f_builds ('+',userid,"crystal", +1)
						bot.send_message(call.message.chat.id, (f"Рабочие нашли странный кристал\n нужно бы обследовать его"))
					elif(sid<300):
						bot.send_message(call.message.chat.id, (f"Все експедиторы погибли в лесу"))
					f_builds ('+',userid,"exped", -1)	
				else:
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает людей!\n /work")
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="У вас уже отправленна експедиция!\n /work")


		
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