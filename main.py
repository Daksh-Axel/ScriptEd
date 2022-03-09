#import statement


from flask import Flask, render_template, request, jsonify , flash
from flask_cors import cross_origin
from itertools import zip_longest
import datetime
import smtplib, ssl
import urllib.request
t_list={}
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/email')
def email_render():
    return render_template("email.html")
@app.route('/todo_list')
def todo_list_render():
    return render_template("todo.html")



@app.route("/submitJSON1", methods=["POST"])
def processJSON1():
     
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr) 
    
    response = ""
    
    # to be followe in template of web page 
    s_email=jsonObj['s_email']
    passw=jsonObj['passw']
    r_email=jsonObj['r_email']
    mess=jsonObj['mess']
    
    
    #support for only gmail
    def email():
        port = 465 
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(s_email, passw) 
            server.sendmail(s_email, r_email, mess)
    email()
    
    return 'Done'


