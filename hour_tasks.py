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
from funs import f_builds


DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')


def hour_tasks_cron():
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()		
	cursor.execute(f"select user_id from users where id > 0")	
	for userid in cursor:
		pop=f_builds ('?', userid[0], "population growth", 0)	
		#print (pop)
		bot.send_message(userid[0], (f"люди + {pop}"))
		
		food_count = f_builds('?',userid[0], "food", 0)
		storage_cap = f_builds('?',userid[0], "storage capacity", 0)
		people= f_builds('?',userid[0], "people", 0)
		food_gr= f_builds('?',userid[0], "food growth", 0)
		food_change = food_gr-(people)*0.1
		
		if((people+pop)<storage_cap):
			f_builds('+',userid[0], "people", raund(pop))
		else:	
			f_builds('=',userid[0], "people", storage_cap)
			
		if((food_change+food_count)<storage_cap):
			f_builds('+',userid[0], "food", raund(food_change))
			print (food_change)
		else:	
			f_builds('=',userid[0], "food", storage_cap)

			
			
	conn.commit()
	conn.close()
