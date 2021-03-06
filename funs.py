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
import datetime

DATABASE_URL = os.environ['DATABASE_URL']
bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')
server = Flask(__name__)

def create_task(userid, f_time,act):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	now=time.time()
	now+=f_time
	act=json.dumps(act)
	cursor.execute(f"INSERT INTO tasks (user_id, time, action) VALUES({userid}, {now}, '{act}') ")	
	conn.commit()
	conn.close()

def my_task(userid):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	now=time.time()
	cursor.execute(f"select time from tasks where user_id={userid}")
	tasks=[]
	for task in cursor:
		t_time = task[0] - now
		tasks.append(round(t_time))
	conn.commit()
	conn.close()
	#print(tasks)
	return tasks
	

def f_coin (op,userid, change):
	if op == '?':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select coin from users where user_id={userid}")
		coin = cursor.fetchall()
		coin = coin[0][0]
		conn.commit()
		conn.close()
		return coin
	
	if op == '+':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"UPDATE users SET coin = coin + {change} WHERE user_id={userid}")	
		conn.commit()
		conn.close()
	
def f_builds (op,userid, what, change):
	if op == '?':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select date from users where user_id={userid}")
		jonew = cursor.fetchall()
		jonew = jonew[0][0]
		n_count = jonew["build"][(f"{what}")]
		conn.commit()
		conn.close()
	if op == '+':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select date from users where user_id={userid}")
		jonew = cursor.fetchall()
		jonew = jonew[0][0]
		n_count = jonew["build"][(f"{what}")]	
		jonew["build"][(f"{what}")] = round(n_count + change,3)
		n_count = jonew["build"][(f"{what}")]
		jon=json.dumps(jonew)
		cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
		conn.commit()
		conn.close()
	if op == '=':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select date from users where user_id={userid}")
		jonew = cursor.fetchall()
		jonew = jonew[0][0]
		n_count = jonew["build"][(f"{what}")]	
		jonew["build"][(f"{what}")] = change
		n_count = jonew["build"][(f"{what}")]
		jon=json.dumps(jonew)
		cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
		conn.commit()
		conn.close()	
	return n_count
	
def f_exp (op,userid, what, change):
	if op == '?':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select date from users where user_id={userid}")
		jonew = cursor.fetchall()
		jonew = jonew[0][0]
		n_count = jonew["build"]["exp"][(f"{what}")]
		conn.commit()
		conn.close()
	if op == '+':
		conn = psycopg2.connect(DATABASE_URL, sslmode='require')
		cursor = conn.cursor()
		cursor.execute(f"select date from users where user_id={userid}")
		jonew = cursor.fetchall()
		jonew = jonew[0][0]
		n_count = jonew["build"]["exp"][(f"{what}")]
		jonew["build"][(f"{what}")] = round(n_count + change,3)
		n_count = jonew["build"]["exp"][(f"{what}")]
		jon=json.dumps(jonew)
		cursor.execute(f"UPDATE users SET date = '{jon}' WHERE user_id={userid}")
		conn.commit()
		conn.close()	
	return n_count	
	
	