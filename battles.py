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
import random
from funs import f_coin
from funs import f_builds

DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
server = Flask(__name__)

def defens (userid, mode):
	warrior_count =  f_builds ('?',userid, "warrior", 0)
	if op == 'rand':
		power1 = warrior_count*3
		power2 = rand(3,50)
		if (power1>power2):
		batl_res = round((power1 - power2*(power2/power1))/3)
		return ((f"""
		На крепость напали!
		Твои воины оказались сильнее
		
		Твои Потери:
		{batl_res}
		Потери врага:
		{batl_res}
		
		
		"""), batl_res)	
		else:
		batl_res = warrior_count - power1*(power1/power2)
		return ("lose", batl_res)	
		
		
	