from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def ping():
    return "PONG !, HELLO FROM DAWAA"

def run():
  app.run(host='0.0.0.0',port=5000)

def server():
    t = Thread(target=run)
    t.start()