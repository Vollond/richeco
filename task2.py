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



DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')

def my_tasks_cron():
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	now=time.time()
	cursor.execute(f"select action, user_id, id from tasks where time < {now}")
	del_ids = []
	for act in cursor:
		print (act)
		action = act[0]
		user_id = act[1]
		id = act[2]
		print(action)
		print(user_id)
		print(id)
		del_ids.append(id)
		bot.send_message(user_id, (f"={id}"))
	for id in del_ids:
		cursor.execute(f"delete from tasks where id={id}")
		conn.commit()
		
	conn.close()
	return True 