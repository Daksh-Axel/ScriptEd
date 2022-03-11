import json
import csv
from csv import DictWriter
from flask import Flask, render_template, request, jsonify , flash, redirect
from flask_cors import cross_origin
import pyttsx3
from itertools import zip_longest
import datetime
import smtplib, ssl
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


t_list={}
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/todo', methods=['GET', 'POST'])
def hello_world():
	if request.method=='POST':
		title = request.form['title']
		desc = request.form['desc']
		todo = Todo(title=title, desc=desc)
		db.session.add(todo)
		db.session.commit()
	allTodo = Todo.query.all() 
	return render_template('todo.html', allTodo=allTodo)

@app.route('/todo/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/todo/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/todo")




@app.route("/")
def home():
    return render_template("home.html")


@app.route('/email')
def problem1():
    return render_template("InputOutputQ1.html")





@app.route("/submitJSON1", methods=["POST"])
def processJSON1():
     
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr) 
    
    response = ""
    s_email=jsonObj['s_email']
    passw=jsonObj['passw']
    r_email=jsonObj['r_email']
    mess=jsonObj['mess']
    
    def email():
        port = 465 
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(s_email, passw) 
            server.sendmail(s_email, r_email, mess)
    email()
    
    return 'Done' 


@app.route("/submitJSON3", methods=["POST"])
def processJSON3():
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr) 
    
    city = jsonObj['city']
    def weather():
            if request.method == 'POST':
                city = request.form['city']
                if len(city)<1:
                    flash("Please enter the name of the city", category='error')
            else:
                # for default name mathura
                city = 'Raipur'

    # your API key will come here


    # source contain json data from api
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=32ccbc36dd38bd11edfcf2606480566d').read()

    # converting JSON data to a dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
            "country_code": str(list_of_data['sys']['country']),
            "cityname":str(city),
            "coordinate": str(list_of_data['coord']['lat']) + ' , '
                        + str(list_of_data['coord']['lon']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
    print(data)
    return render_template('InputOutputQ3.html', data = data)


@app.route('/weather',methods=['POST','GET'])
def weather():
    if request.method == 'POST':
            city = request.form['city']
    else:
        # for default name mathura
            city = 'Raipur'

    # your API key will come here
    
    # source contain json data from api
    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=32ccbc36dd38bd11edfcf2606480566d').read()

    # converting JSON data to a dictionary
    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "cityname":str(city),
        "coordinate": str(list_of_data['coord']['lat']) + ' °,'
                    + str(list_of_data['coord']['lon'])+' °',
        "temp": str(round(list_of_data['main']['temp']-273, 2)) + " °C",
        "pressure": str(list_of_data['main']['pressure']) + ' HPa',
        "humidity": str(list_of_data['main']['humidity']) + '%',
    }
    print(data)
    return render_template('InputOutputQ3.html', data = data)



if __name__ == "__main__":
    app.run(debug=True)


