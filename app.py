from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory
import requests
import time
import datetime
import json

app = Flask(__name__, static_url_path='')
    
def predictor(tavg, model):
    y = model['coef'][0][0]*tavg+model['intercept'][0]
    return round(y,0)

@app.route("/", methods=['GET','POST'])
def start():
    return render_template('index.html')
    
    
@app.route("/predict-crime-by-temp", methods=['GET','POST'])
def perdict():
    # load model
    temp = request.args.get('temp')
    if temp == None:
        return "error: no input"
    file = open("model/regression.txt","r") 
    models = json.loads(file.read())
    if int(temp) >= 25:
        model = models['regressor85']
    else :
        model = models['regressor25']
    return str(predictor(int(temp), model))
    
    
@app.route("/three-day-crime-forcastast", methods=['GET','POST'])
def forcast():

    # your code should be inside this founction
    ress = {}
    r = requests.get('https://forecast.weather.gov/MapClick.php?lat=42.3587&lon=-71.0567')
    lines = r.text.split('\n')
    dc = 0
    pc = 0
    d = 0
    conditions = []
    for line in lines:
        if '<div class="tombstone-container"' in line:
            dc += 1
        if '<p>' in line:
            pc+=1
        if 'temp' in line and dc == 1 :
            check = line
            if check.split('alt="')[1].split(":")[0] == 'Today':
                n = 1
            else: 
                n = 2
        if 'temp' in line and dc > 0 and dc == n :
            condition = {}
            condition['day'] = d
            condition['temp high'] = int(line.split('temp ')[1].split(' &deg;')[0][-2:])
        if 'temp' in line and dc > 0 and dc == n+1 :
            condition['temp low'] = int(line.split('temp ')[1].split(' &deg;')[0][-2:])
            conditions.append(condition)
            d += 1
            n += 2
            
    # this is the result i need, should be around 5-10 days
    # ress = {day:'', tempurature:''}
            
    
    file = open("model/regression.txt","r") 
    models = json.loads(file.read())
            
    today = datetime.date.today()
    n = 0
    for condition in conditions:
        if condition['day'] == n:
            ress[str(n)] = {}
            ress[str(n)]['day'] = time.mktime((today + datetime.timedelta(hours=24*n)).timetuple())
            ress[str(n)]['thigh'] = condition['temp high']
            ress[str(n)]['tlow'] = condition['temp low']
            ress[str(n)]['tavg'] = (condition['temp high'] + condition['temp low'])/2
            if ress[str(n)]['tavg'] >= 25:
                model = models['regressor85']
            else :
                model = models['regressor25']            
            ress[str(n)]['numcrime'] = predictor(ress[str(n)]['tavg'], model)
            n += 1
    return render_template('forcast.html', len = len(ress), ress = ress)


if __name__ == "__main__":
    app.run(host= '127.0.0.1',debug=True)