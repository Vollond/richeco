import telebot
import os
from flask import Flask, request
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']



bot = telebot.TeleBot('610980315:AAE494y1vZOwGeNmisevy-3OtcMwJD_JpVs')

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Helo, ' + message.from_user.first_name)

@bot.message_handler(commands=['ping'])
def start(message):
    bot.send_message(chatid, 'pong, ' + message.from_user.first_name)

@bot.message_handler(commands=['work'])
def start(message):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute("UPDATE users SET coin = coin + 1 WHERE name='nit'")
	conn.commit()
	cursor.execute("select coin from users where name='nit'")
	results = cursor.fetchall()
	conn.close()
	bot.send_message(chatid, 'pong, ' + message.from_user.first_name)

	
@bot.message_handler(commands=['new'])
def start(message):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute("insert into users (name,coin) values('nit','10')")
	conn.commit()
	conn.close()
	bot.reply_to(message, 'pong, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)



	

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