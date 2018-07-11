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
from telegramcalendar import create_calendar
import datetime
from funs import create_task
from funs import my_task
from task2 import my_tasks_cron


DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
server = Flask(__name__)

@bot.message_handler(commands=['wr1'])
def start(message):
	bot.send_message(message.chat.id, (f"""
Рабочие нашли помятый кусок свитка: 
`Оно [ça]` 
	"""), parse_mode='Markdown')
	msgid=message.message_id+1
	time.sleep(1) 	
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"""
Рабочие нашли помятый кусок свитка: 
`Оно [ça] * функционирует повсюду, иногда без остановок, иногда с перерывами.` 
	"""), parse_mode='Markdown')
	time.sleep(1) 		
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"""
Рабочие нашли помятый кусок свитка: 
`Оно [ça] * функционирует повсюду, иногда без остановок, иногда с перерывами. 
Оно дышит, оно греет, оно ест.` 
	"""), parse_mode='Markdown')
	time.sleep(1) 	
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"""
Рабочие нашли помятый кусок свитка: 
`Оно [ça] * функционирует повсюду, иногда без остановок, иногда с перерывами. 
Оно дышит, оно греет, оно ест. 
Оно испражняется, оно целует.` 
	"""), parse_mode='Markdown')
	time.sleep(1) 	
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"""
Рабочие нашли помятый кусок свитка: 
`Оно [ça] * функционирует повсюду, иногда без остановок, иногда с перерывами. 
Оно дышит, оно греет, оно ест. 
Оно испражняется, оно целует.
Но какое заблуждение говорить о нем как о чем-то одном и определенном [le ça].` 
	"""), parse_mode='Markdown')
	time.sleep(1) 	

def task_test():
	bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
	bot.send_message(322682583, "таск")	

@bot.message_handler(commands=['task'])
def start(message):
	bot.send_message(322682583, "таск")	
	
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Helo, ' + message.from_user.first_name)
	
@bot.message_handler(commands=['ping'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text="""
	'123' `inline fixed-width code`11''2312*bold text*3
	1''2312123
	""", parse_mode='Markdown')
	
@bot.message_handler(commands=['help'])
def start(message):
	t1 = time.time()
	bot.reply_to(message, """
	/me
	""")
	print(time.time() - t1)

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
	jon["build"]["exp"]=0
	jon=json.dumps(jon)
	cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
	conn.commit()
	conn.close()
	
@bot.message_handler(commands=['upd']) 
def start(message):
	userid = message.from_user.id
	
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute(f"select date from users where user_id={userid}")
	jonew = cursor.fetchall()
	jon = jonew
	print (jon)
	print(jon[0][0])
	jon[0][0]["build"]["people"]=10
	jon[0][0]["build"]["population growth"]=1
	jon[0][0]["build"]["food"]=5
	jon=json.dumps(jon[0][0])
	cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
	conn.commit()
	conn.close()	
	

@bot.message_handler(func=lambda mess: mess.text=='work' and mess.content_type=='text')
def default_test(message):
	keyboard = types.InlineKeyboardMarkup()
	work_button = types.InlineKeyboardButton(text="Кликай, чтобы заработать!", callback_data="work")
	exped_button = types.InlineKeyboardButton(text="Отправить 5 человек в шахту", callback_data="mine")
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
	t1 = time.time()
	userid = message.from_user.id
	keyboard = types.InlineKeyboardMarkup()
	n_count =  f_builds ('?',userid,"n",0)
	n_cost = 100
	work_button = types.InlineKeyboardButton(text=(f"N-центр"), callback_data="N")
	workers_button = types.InlineKeyboardButton(text=(f"Рабочих"), callback_data="workers")
	warrior_button = types.InlineKeyboardButton(text=(f"Воинов"), callback_data="warrior")
	keyboard.add(work_button)
	keyboard.add(workers_button)
	keyboard.add(warrior_button)
	bot.send_message(message.chat.id, (f"""
	Построить чет?
	Строить N-центр\n за ${n_cost}
	Строить Рабочих\n за $10
	Строить Воинов\n за $50
	"""), reply_markup=keyboard)
	print(time.time() - t1)

@bot.message_handler(func=lambda mess: mess.text=='me' and mess.content_type=='text')	
def default_test(message):
	t1 = time.time()
	my_tasks_cron()
	userid = message.from_user.id
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	if (f_builds ('?',userid, "n", 0)>1):
		exped="exped"
	else: 
		exped="xxxx"
	if (f_builds ('?',userid, "crystal", 0)>1):
		research="research"
	else:
		research="xxxx"
	markup.row('work', (f"{exped}"),'laboratory')
	markup.row('me', 'build', (f"{research}"))
	userid = message.from_user.id
	coin =  f_coin ('?',userid, 0)
	n_count =  f_builds ('?',userid,"n",0)
	workers_count =  f_builds ('?',userid, "workers", 0)
	warrior_count =  f_builds ('?',userid, "warrior", 0)
	people_count =  round(f_builds ('?',userid, "people", 0),1)
	people_count =  round(f_builds ('?',userid, "food", 0),1)
	population_count =  f_builds ('?',userid, "population growth", 0)
	coin =  f_coin ('?',userid, 0)
	m_task=my_task(userid)
	i=0
	if (len(m_task)>0):
		task_str = "Задачи:\n"
		while (i<len(m_task)):
			task_str += (f"{m_task[i]}\n")
			i+=1
	else:
		task_str=''
	bot.send_message(message.chat.id, (f"""
	👥 {people_count}  🍕{food}  💰{coin} 
	{task_str}

	
	Постройки: 
	N-центры = {n_count}

	Прирост населения {population_count}/час
	Рабочих = {workers_count} 
	Воинов = {warrior_count}"""),reply_markup=markup)
	print(time.time() - t1)

	
	
@bot.message_handler(func=lambda mess: mess.text=='laboratory' and mess.content_type=='text')	
def default_test(message):
	t1 = time.time()
	userid = message.from_user.id
	jon = _default_data()
	jon["build"]["exp"]["+"]=1
	create_task(userid,660,jon)
	
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.row('Начать исследование')
	markup.row('me')
	bot.send_message(message.chat.id, (f"""
	Исследования приблизят вас к новым технологиям и возможностям
	
	
	"""),reply_markup=markup)
	print(time.time() - t1)
	


@bot.message_handler(func=lambda mess: mess.text=='research' and mess.content_type=='text')	
def default_test(message):
	userid = message.from_user.id
	bot.send_message(message.chat.id, (f"◽️◽️◽️◽️◽️◽️◽️◽️◽️"))
	msgid=message.message_id+1
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◽️◽️◽️◽️◽️◽️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◽️◽️◽️◽️◽️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◽️◽️◽️◽️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◽️◽️◽️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◽️◽️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◽️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◽️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◾️◽️"))
	time.sleep(3) 
	bot.edit_message_text(chat_id=message.chat.id, message_id=msgid, text=(f"◾️◾️◾️◾️◾️◾️◾️◾️◾️"))
	bot.send_message(message.chat.id, (f"Теперь вы можете нечто новое...."))



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
			n_cost=100
			if int(coin) >= n_cost:
				f_coin ('+',userid, - n_cost)
				n_count =  f_builds ('+',userid,"n", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="N")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} N-центров \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет!")
				
		if call.data == "workers":
			coin =  f_coin ('?',userid, 0)
			work_count =  f_builds ('?',userid, "workers", 0)
			n_cost=10
			p_count =  f_builds ('?',userid, "people", 0)
			if (int(coin) >= n_cost) and (int(p_count) >= 1):
				f_coin ('+',userid, - n_cost)
				f_builds ('+',userid,"people", -1)
				work_count =  f_builds ('+',userid,"workers", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="workers")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {work_count} рабочих \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет или людей!")
				
		if call.data == "warrior":
			coin =  f_coin ('?',userid, 0)
			n_count =  f_builds ('?',userid, "warrior", 0)
			p_count =  f_builds ('?',userid, "people", 0)
			n_cost=50
			if int(coin) >= n_cost and p_count >= 1 :
				f_coin ('+',userid, -n_cost)
				f_builds ('+',userid,"people", -1)
				n_count =  f_builds ('+',userid,"warrior", 1)
				keyboard = types.InlineKeyboardMarkup()
				work_button = types.InlineKeyboardButton(text=(f"Строим еще за {n_cost}?"), callback_data="warrior")
				keyboard.add(work_button)
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=(f"Есть {n_count} воинов \nСтроим еще за {n_cost}?"),reply_markup=keyboard)
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает монет или людей!")

				

			
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
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает людей!")
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="У вас уже отправленна експедиция!")
		
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
					else:
						f_builds ('+',userid,"workers", +20)
						bot.send_message(call.message.chat.id, (f"В этот раз експедиция вернулась с пустыми руками"))
					f_builds ('+',userid,"exped", -1)	
				else:
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает людей!")
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="У вас уже отправленна експедиция!")
	
		if call.data == "unknown_place":
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
						bot.send_message(chat_id=message.chat.id, text=(f"""Рабочие нашли: 
						'Оно [ça] * функционирует повсюду, иногда без остановок, иногда с перерывами. 
						Оно дышит, оно греет, оно ест. 
						Оно испражняется, оно целует. 
						Но какое заблуждение говорить о нем как о чем-то одном и определенном [le ça].' 
						"""), parse_mode='Markdown')
					elif(sid<300):
						bot.send_message(call.message.chat.id, (f"Все експедиторы погибли в лесу"))
					else:
						f_builds ('+',userid,"workers", +20)
						bot.send_message(call.message.chat.id, (f"В этот раз експедиция вернулась с пустыми руками"))
					f_builds ('+',userid,"exped", -1)	
				else:
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Не хватает людей!")
			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="У вас уже отправленна експедиция!")				

########################
current_shown_dates={}
@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Please, choose a date", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime.datetime(int(saved_date[0]),int(saved_date[1]),int(day),0,0,0)
        bot.send_message(chat_id, str(date))
        bot.answer_callback_query(call.id, text="")

    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
#######################		
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
application.listen(environ["PORT"])