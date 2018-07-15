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



conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()		
cursor.execute(f"select user_id from users where id > 0")	
for userid in cursor:
	userid=userid[0]
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute(f"select date from users where user_id={userid}")
	jonew = cursor.fetchall()
	jon = jonew
	print (jon)
	print(jon[0][0])
	jon[0][0]["build"]["max_researchers"]=3
	jon[0][0]["build"]["exp"]["a"]=0

	
	jon=json.dumps(jon[0][0])
	cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
	conn.commit()
	conn.close()	
		
conn.commit()
conn.close()
