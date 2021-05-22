from flask import Flask, make_response,render_template
import json
from datetime import datetime

from data import  dictionaryRegion, dictionaryParametrs
import model
import classifier

app = Flask(__name__)

mod = model.Model()
cl = classifier.AccidentPredictor()
@app.route('/')
def hello_world():
    reg =[{"id":"RU-KDA","danger": "34"}];
    js =  json.dumps(reg)
    res = make_response(js)
    res.headers['Content-Type']= 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res

@app.route('/reg/<id>/<date>')
def region_inf(id,date):
    date = datetime.strptime(date, "%Y-%m-%d")
    kol = mod.get_subjects_by_date(date.date())
    region ={"Region": dictionaryRegion[id],"Objects":[]}
    row =0
    for i in kol:
        if i.event is not None and i.subject==id:
            region["Objects"].append({"p1":i.type,"p2": "44.968372, 39.831685","id": row,"speed":str(i.wind_speed),"temp":str(i.temperature)})
            region["Event"]= i.event
            print("Test "+ i.event)
            region["Description"] = i.description
            row+=1
            # print(i.description)
            # print(i.wind_speed)
            # print(i.temperature)
    jSon = json.dumps(region)
    res = make_response(jSon)
    res.headers['Content-Type'] = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/weather/<id>/<date>')
def par_Weather(id,date):
    kl = cl.predict_all()
    print(kl["RU-KDA"].fire_proba)
    region = {}
    for i in kl:
        print(i," - ", kl[i])
        if i == id:
            region["Region"]= i
            region["fire_proba"] = "{:.4}".format(kl[i].fire_proba)
            region["ice_proba"] = "{:.4}".format(kl[i].ice_proba)
            region["norm_proba"] = "{:.4}".format(kl[i].norm_proba)
            region["tree_fall_proba"] = "{:.2}".format(kl[i].tree_fall_proba)
            region["temp"] = str(kl[i].weather.temp)
            region["speeding"] = str(kl[i].weather.windspeed)
    jSon = json.dumps(region)
    res = make_response(jSon)
    res.headers['Content-Type'] = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res



@app.route('/par/<id>')
def par_Object(id):
    par= dictionaryParametrs[id]
    # par = {"name":"АЭС","Par":{"par1":44,"par2": "fgvdsgdf"}}
    jSon = json.dumps(par)
    res = make_response(jSon)
    res.headers['Content-Type'] = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/date/<date>')
def date_contr(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    kol =  mod.get_subjects_by_date(date.date())
    list = []
    for i in kol:
        if i.event is not None:
            print(i)
            dict = {"id":i.subject}
            list.append(dict)
      #  print(i.date+" | "+ i.subject +" | "+ i.temperature  +" | "+ i.wind_speed +" | "+ i.event  +" | "+ i.description +" | "+ i.type)
            print(i.subject)

    reg = list
    js = json.dumps(reg)
    res = make_response(js)
    res.headers['Content-Type'] = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res



@app.route('/weather/')
def pars_Weather():
    kl = cl.predict_all()
#    print(kl["RU-KDA"].fire_proba)
    regions =[]

    for i in kl:
        print(i," - ", kl[i])
        region = {}
        region["Region"]= i
        region["fire_proba"] = "{:.4}".format(kl[i].fire_proba)
        region["ice_proba"] = "{:.4}".format(kl[i].ice_proba)
        region["norm_proba"] = "{:.4}".format(kl[i].norm_proba)
        region["tree_fall_proba"] = "{:.2}".format(kl[i].tree_fall_proba)
        region["temp"] = str(kl[i].weather.temp)
        region["speeding"] = str(kl[i].weather.windspeed)
        regions.append(region)
    jSon = json.dumps(regions)
    res = make_response(jSon)
    res.headers['Content-Type'] = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

# @app.route('/kr')
# def kr_svg():
#     res =make_response('kr_svg.html')
#     res.headers['Content-Type'] = 'application/json'
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     return res


if __name__ == '__main__':
    app.run()
