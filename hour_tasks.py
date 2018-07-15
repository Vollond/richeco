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
		
		food_count = f_builds('?',userid[0], "food", 0)
		storage_cap = f_builds('?',userid[0], "storage capacity", 0)
		people= f_builds('?',userid[0], "people", 0)
		food_gr= f_builds('?',userid[0], "food growth", 0)
		food_change = food_gr-(people)*0.1
		
		if((people+pop)<storage_cap):
			f_builds('+',userid[0], "people", pop)
		else:	
			f_builds('=',userid[0], "people", storage_cap)
			
		if((food_change+food_count)<storage_cap):
			f_builds('+',userid[0], "food", food_change)
			print (food_change)
		else:	
			f_builds('=',userid[0], "food", storage_cap)
			
			
		researchers = f_builds('?',userid[0], "researchers", 0)
		max_researchers = f_builds('?',userid[0], "max_researchers", 0)
		cof=researchers/max_researchers
		n = f_builds('?',userid[0], "n", 0)
		lvl_exp = random.randint(1,2)
		if (random.randint(1,100)<(5*cof)):
			n=n+1
			break
		if((random.randint(1,100)<(20*cof)):
			exp(n,3)
			break			
		elif((random.randint(1,100)<(50*cof)):
			exp(n,2)
			break	
		else:
			exp(n,1)
			break
			
			
	conn.commit()
	conn.close()
