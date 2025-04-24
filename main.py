import requests
import telebot
import json
from server import server
import time
import socket
import psutil
from os import environ

bot_key = environ['BOT_KEY']
bot = telebot.TeleBot(bot_key)

print("i`am running now!")
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
  user_id = message.from_user.id
  
  try:
    user_username = message.from_user.username
  except:
    user_username = "unknow"

  try:
    requests.post('https://tel-api.serv00.net/api.php',
                  json={
                    "rq": "dawaa",
                    "tel_id": user_id,
                    "username": user_username
                  })
  except:
    pass

  bot.send_message(
    message.chat.id,
    "مرحباً بك في دواء مصر , يرجى كتابة اسم الدواء بشكل صحيح ومختصر",
    parse_mode='Markdown')
  # bot.send_message(message.chat.id, infotip, parse_mode= 'Markdown' )


#answering every message not just commands
def isMSg(message):
  return True

@bot.message_handler(func=isMSg)
def reply(message):
  words = message.text
  if len(words) < 3:
    return bot.reply_to(message, "الاسم صغير جدا")
  if len(words) > 60:
    return bot.reply_to(message, "الاسم كبير جدا")
  else:
    try:
      dawaa_name = words
      headers = { 
        'Content-Type' : "application/x-www-form-urlencoded; charset=UTF-8",
        'Accept' : '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
      }
      res = requests.post('https://dwaprices.com/routing.php',
                          data={
                            'search': '1',
                            'searchq': dawaa_name,
                            'order_by': 'name ASC'
                          },headers=headers)

      results55 = res.text
      results = json.loads(results55)
      results = results['data']
      message22 = ""
      if len(results) < 1:
        print("NOT FOUND 1")
        noneVar = results['noneVar']
      else:
        for i in range(0, len(results)):

          arabic = results[i]['arabic']
          if results[i]['arabic'] == "":
            arabic = results[i]['name']

          price = results[i]['price']
          uses = ""
          uses1 = results[i]['uses']
          if results[i]['uses'] != "":
            uses = "*دواعي الاستخدام* : {} \n".format(uses1)

          txt1 = '\n *اسم الدواء* : {} \n'\
              '*السعر* : {} جنية مصري \n'\
              '{} \n'\
              '---------------------------------- \n'.format(arabic, price, uses)
          message22 = message22 + txt1
        try:
            if message.from_user.username != '' and message.from_user.username != None:
                message_text = f"User @{message.from_user.username} search for '{dawaa_name}'"
            else:
                message_text = f"User '{message.from_user.id}' searching for '{dawaa_name}'"
            bot.send_message('1549082019', message_text)
        except:
            pass

        return bot.reply_to(message, message22, parse_mode='Markdown')

    except Exception as ii:
      print("WE HAVE AN ERROR! >> ")
      print(ii)
      dawaa_name = words
      res = requests.get(
        'https://v-gateway.vezeetaservices.com/inventory/api/V2/ProductShapes?query={}&from=1&size=10&isTrending=false&Version=2'
        .format(dawaa_name))

      results55 = res.text

      results = json.loads(results55)
      results = results['productShapes']
      message22 = ""

      if len(results) < 1:
        return bot.reply_to(
          message,
          "يرجى كتابة اسم الدواء بشكل صحيح \nاو جرب كتابته باللغة الانجليزية.")
      else:
        for i in range(0, len(results)):

          arabic = results[i]['productNameAr']
          if results[i]['productNameAr'] == "":
            arabic = results[i]['productUrlEn']

          price = results[i]['newPrice']
          uses = ""
          uses1 = results[i]['categoryUrlAr']
          if results[i]['categoryUrlAr'] != "":
            uses = "*الوصف* : {} \n".format(uses1)

          txt1 = '\n *اسم الدواء* : {} \n'\
              '*السعر* : {} جنية مصري \n'\
              '{} \n'\
              '---------------------------------- \n'.format(arabic, price, uses)
          message22 = message22 + txt1
        try:
          if message.from_user.username != '' and message.from_user.username != None:
              message_text = f"User @{message.from_user.username} search for '{dawaa_name}'"
          else:
              message_text = f"User '{message.from_user.id}' searching for '{dawaa_name}'"
          bot.send_message('1549082019', message_text)
        except:
          pass
        return bot.reply_to(message, message22, parse_mode='Markdown')



# KILL PORT 5000
def kill_port(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            try:
                process = psutil.Process(conn.pid)
                process.terminate()
            except psutil.NoSuchProcess:
                pass
              
try:              
  kill_port(5000)
except Exception as ii2:
  print(ii2)
  pass

server()
bot.infinity_polling()
# bot.polling()