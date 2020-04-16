import telebot 
from telebot import types 
import mysql.connector
import datetime


mydb = mysql.connector.connect(
  host="host",
  user="USER",
  passwd="PWD",
  database="DB"
)

mycursor = mydb.cursor()
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
# print(yesterday)

def get_order_amount(mobile):
    mob = mobile
    # print(mob)
    sql =f"""SELECT distinct c.Mobile, o.client_id, COUNT(*) orders
      FROM max_taxi_incoming_orders o
      JOIN max_taxi_server_clients  c
      ON c.ClientID = o.client_id
      WHERE o.status = 7
      AND o.order_finished_time > '{yesterday}'
      AND c.Mobile = {mob}
      GROUP BY 1
      ORDER BY 3 DESC
      limit 15"""
    
    mycursor.execute(sql)
    column = mycursor.fetchall()
    
    if len(column) == 0:
        msg = 'Check the number again, the result is empty'
    else:
        msg = f'Number: {column[0][0]}\nClient_ID: {column[0][1]}\nOrders/day: {column[0][2]}'
    #msg='privet'
    return msg


TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(regexp=r"(9989)[0-9]{8}",)
def first_opt(message):
    chat_id = message.chat.id
    mobile = message.text
    msg = get_order_amount(mobile)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(None, regexp=r"^(9)[0-9]{8}$")
def second_opt(message):
    chat_id = message.chat.id
    mobile = '998'+ message.text
    msg = get_order_amount(mobile)
    bot.send_message(chat_id, msg)
    return


@bot.message_handler(content_types=['text'])
def error_message(message):
    chat_id = message.chat.id
    msg = 'Error message!\nIt should be in forms given below:\n9989ABBBCCDD\n9ABBBCCDD'
    bot.send_message(chat_id, msg)
    return


if __name__ == "__main__":
    bot.polling(None)
