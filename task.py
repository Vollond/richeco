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
bot.send_message(322682583, "таск")	

i=0
while (i<9):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	now=time.time()
	cursor.execute(f"select action, user_id, id from tasks where time < {now}")
	act = cursor.fetchall()
	print (act)
	print (action) = act[0][0]
	print (user_id) = act[0][1]
	print (id) = act[0][2]
	#cursor.execute(f"delete from tasks where id={id}")
	bot.send_message(322682583, (f"={id}"))	
	conn.commit()
	conn.close()
	time.sleep(60) 	
	i+=1

'''
print ('1')
import main
print ('2')
from main import task_test
task_test()
print ('123')
task_test()
'''