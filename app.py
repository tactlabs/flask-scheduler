from flask import Flask, render_template
import os
import sys
from flask import request
from random import randint

import atexit
from apscheduler.scheduler import Scheduler
from flask import Flask

import datetime

import logging

app = Flask(__name__)

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()


@cron.interval_schedule(seconds = 5)
def job_function():
    # Do your work here
    now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    app.logger.error(now)
    #app.logger.error(type(now))
    #app.logger.error('inside job : ')

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))

@app.route('/')
def home():
    app.logger.error('inside home')
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def result():
    
    value1  = int(request.form.get('value1'))
    value2  = int(request.form.get('value2'))
    
    # You can validate the car brands. If someone is telling the wrong brand name, reply them with the wrong answer
    
    value3 = add(value1, value2)
    
    result = {
        'value1' : value1,
        'value2' : value2,
        'value3': value3
    }
    
    #return content
    return render_template('result.html', result=result)

def add(value1, value2):
    return value1 + value2

if __name__ == "__main__":
    app.run()
