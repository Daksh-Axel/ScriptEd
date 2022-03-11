
#import statement

import json
import csv
from csv import DictWriter
from flask import Flask, render_template, request, jsonify , flash
from flask_cors import cross_origin
import pyttsx3
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



@app.route("/submitJSON2", methods=["POST"])
def processJSON2():
    jsonStr = request.get_json()
    jsonObj = json.loads(jsonStr) 
    
    response = ""
    date=jsonObj['date']
    work=jsonObj['work']
    time=jsonObj['time']
    option=jsonObj['yn']

    def text_to_speech(text, gender):
        voice_dict = {'Male': 0, 'Female': 1}
        code = voice_dict[gender]
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
            
    if date not in t_list.keys():
        t_list[date]=[]
        t_list[date].append([work,time])
        text_to_speech('New date along with work to be done has been added','Female')
    else:
        t_list[date].append([work,time])   
        text_to_speech('Work has been added','Female')
        
    if option[0]=='n':
        text_to_speech('Thank You, your data has been stored','Female')
    else:
        text_to_speech('Please make more entries','Female')
        
    data=[]
    name=[' ']
    work={}
    times={}
   
    for key in t_list:
        work[key]=[]
        times[key]=[]
        for i in range(len(t_list[key])):
            work[key].append(t_list[key][i][0])
            times[key].append(t_list[key][i][1])
    
    
    for key in t_list:
        data.append(times[key])       
        data.append(work[key])
        data.append(' ')
        name.append(key)
        name.append(' ')
        name.append(' ')
        export_data = zip_longest(*data, fillvalue = '')
    with open('Data.csv', 'w', encoding="ISO-8859-1", newline='') as file:
        write = csv.writer(file)
        write.writerow(tuple(name))
        write.writerows(export_data)
   
    return response

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
        "coordinate": str(list_of_data['coord']['lat']) + ' , '
                    + str(list_of_data['coord']['lon']),
        "temp": str(list_of_data['main']['temp']) + ' K',
        "pressure": str(list_of_data['main']['pressure']) + ' HPa',
        "humidity": str(list_of_data['main']['humidity']) + '%',
    }
    print(data)
    return render_template('weather.html', data = data)

if __name__ == "__main__":
    app.run(debug=True)


