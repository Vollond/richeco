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

DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
server = Flask(__name__)

def f_coin (op,userid):
	if op = '?':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select coin from users where user_id={userid}")
		coin = cursor.fetchall()
		coin = coin[0][0]
		conn.commit()
		conn.close()
	return coin