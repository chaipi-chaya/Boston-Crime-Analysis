from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory
import requests
import json

app = Flask(__name__, static_url_path='')
    
def predictor(tavg, model, degree):
    if degree == 3:
        y = model['coef'][0][3]*(tavg**3) + \
            model['coef'][0][2]*(tavg**2) + \
            model['coef'][0][1]*(tavg) + \
            model['intercept'][0]
    if degree == 4:
        y = model['coef'][0][4]*(tavg**4) + \
            model['coef'][0][3]*(tavg**3) + \
            model['coef'][0][2]*(tavg**2) + \
            model['coef'][0][1]*(tavg) + \
            model['intercept'][0]
    return round(y,0)

@app.route("/", methods=['GET','POST'])
def start():
    return render_template('index.html')

@app.route("/code_explanation", methods=['GET','POST'])
def explanation():
    return render_template('code_explanation.html')

@app.route("/web_scraping", methods=['GET','POST'])
def scraping():
    return render_template('web_scraping.html')

@app.route("/preprocessing", methods=['GET','POST'])
def preprocessing():
    return render_template('data_preprocess.html')

@app.route("/analyzing", methods=['GET','POST'])
def analyzing():
    return render_template('data_analysis_overall.html')
    
@app.route("/regression", methods=['GET','POST'])
def regression():
    return render_template('regression_analysis.html')
    
@app.route("/pattern", methods=['GET','POST'])
def pattern():
    return render_template('crime_pattern_analysis.html')
    
@app.route("/short_patrol", methods=['GET','POST'])
def short_patrol():
    return render_template('shortest_patrol_route.html')
    
@app.route("/markov_chain_demo", methods=['GET','POST'])
def mcdemo():
    file = open("model/MC_and_lamda.txt","r") 
    data = json.loads(file.read())
    return render_template('markov_chain_demo.html', data = data)
    
@app.route("/regression_api", methods=['GET','POST'])
def regression_api():
    return render_template('regression_api.html')
    
    
    
@app.route("/predict_crime_by_temp", methods=['GET','POST'])
def perdict():
    # load model
    temp = request.args.get('temp')
    if temp == None:
        return "error: no input"
    file = open("model/regression.txt","r") 
    models = json.loads(file.read())
    if float(temp) >= 25:
        degree = 4
        model = models['regressorpoly4']
    else :
        degree = 3
        model = models['regressorpoly325']
    return str(predictor(float(temp), model, degree))
    
    
@app.route("/crime_forecast", methods=['GET','POST'])
def forecast():

    r = requests.get('https://weather.com/weather/tenday/l/Boston+MA?canonicalCityId=6320cadd3d539b434b5a45c094becf3edbe8ea88958185a2287a801115c9ae30')
    lines = r.text.split('\n')

    conditions = []
    n = 0
    for line in lines:
        if '<td class="temp" headers="hi-lo"' in line:
            n += 1
            if n == 1:
                continue
            condition = {}
            if len(line.split("</tr>")) == 2:
                condition['day'] = line.split('<span class="day-detail')[1].split("</span>")[0].split('>')[1]
                hi = line.split('<td class="temp" headers="hi-lo"')[1].split("</sup>")[0].split('<span class="">')[1].split('<sup>')[0]
                low = line.split('<td class="temp" headers="hi-lo"')[1].split("</sup>")[1].split('<span class="">')[1].split('<sup>')[0]
                condition['temp'] = (float(hi)+float(low))/2
                conditions.append(condition)
            else :
                tr = line.split("</tr>")
                for i in range(len(tr)):
                    condition = {}
                    if i < len(tr) - 1:
                        condition['day'] = tr[i].split('<span class="day-detail')[1].split("</span>")[0].split('>')[1]
                        td = tr[i].split("hi-lo")
                        hi = td[1].split("</sup>")[0].split('<span class="">')[1].split('<sup>')[0]
                        low = td[1].split("</sup>")[1].split('<span class="">')[1].split('<sup>')[0]
                        condition['temp'] = (float(hi)+float(low))/2
                        conditions.append(condition)
    
    crimes = []
    temps = []
    days = []
    file = open("model/regression.txt","r") 
    models = json.loads(file.read())
    for i in conditions:
        if float(i['temp']) >= 25:
            degree = 4
            model = models['regressorpoly4']
        else :
            degree = 3
            model = models['regressorpoly325']
        days.append(i['day'])
        temps.append(i['temp'])
        crimes.append(float(predictor(float(i['temp']), model, degree)))
    return render_template('forecast.html', days = days, temps = temps, crimes = crimes)

import webbrowser
webbrowser.open_new_tab("http://localhost:5000/")

if __name__ == "__main__":
    app.run(host= '127.0.0.1',debug=False)
    
    