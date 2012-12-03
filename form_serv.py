from flask import Flask, session, request, render_template, g, redirect, send_file
import basic_form as bform
import random
import simplejson as json
#import md5
import traceback
import socket
import sys
import uuid
import websocket
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
app = Flask(__name__)

@app.route('/reg/', methods=["POST", "GET"])
def get_data2():
    return render_template('register.html')

@app.route('/login/', methods=["POST"])
def register(request):
    form = RegistrationForm(request.POST)
    if form.validate():
        print "received username:",form.username.data
        print "received email:",form.email.data
        print "accept rules:",form.accept_rules.data
