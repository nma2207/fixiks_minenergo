import joblib
import yaweather.cities

import utils
from yaweather.models.response import Response
from yaweather.models.base import PhenomCondition
from yaweather.models.base import PrecipitationType
from yaweather import YaWeather

import pandas as pd
import numpy as np
def get_winddir(winddir):
    degrees = {
        'n': 0,
        'ne': 45,
        'e': 90,
        'se': 135,
        's' : 180,
        'sw': 225,
        'w': 270,
        'nw': 315,
        'c': 0
    }
    return degrees[winddir]

def check_condition_type(condition, types):
    if condition is None:
        return 0
    elif condition in types:
        return 1
    else:
        return 0

class Weather:
    def __init__(self, responce: Response):
        if responce is None:
            return
        #координаты
        self.lon = responce.info.lon
        self.lat = responce.info.lat
        #температура
        self.temp = responce.fact.temp
        #направление ветра
        self.winddir = get_winddir(responce.fact.wind_dir)
        #скорость ветра
        self.windspeed = responce.fact.wind_speed

        forecast = responce.forecasts[0]
        #осадки
        self.precipitation = forecast.prec_mm if forecast.prec_mm is not None else 0
        #снег
        self.snowstorm = check_condition_type(responce.fact.phenom_condition,
                                              [PhenomCondition.drifting_snow, PhenomCondition.blowing_snow, PhenomCondition.ice_pellets])
        #туман
        self.mist = check_condition_type(responce.fact.phenom_condition, [PhenomCondition.fog, PhenomCondition.mist, PhenomCondition.smoke])
        #град
        self.hail = check_condition_type(responce.fact.prec_type, [PrecipitationType.hail])
        #еще какой-то град
        self.glaze_ice = check_condition_type(responce.fact.phenom_condition, [PhenomCondition.ice_pellets])
        #порывы ветра?
        self.blast = 0
        self.squall = 0
        self.storm_rainfall = 0
        #гроза
        self.electric_storm = int(responce.fact.is_thunder) if responce.fact.is_thunder is not None else 0

    def get_data(self):
        data = np.array([self.lon, self.lat, self.temp, self.winddir, self.windspeed, self.precipitation, self.snowstorm, self.mist,
                self.hail, self.glaze_ice, self.blast, self.squall, self.storm_rainfall, self.electric_storm])
        return data.reshape(1,1,14)

class Classifier:
    classifier_filename = "classifier.joblib"

    def __init__(self):
        self.classifier = joblib.load(self.classifier_filename)

    def predict_accident(self, data):
        #print(self.classifier.classes_)
        return self.classifier.predict_proba(data)*100


class AccidentPredictionData:
    def __init__(self, weather, ice_proba, norm_proba, tree_fall_proba, fire_proba):
        self.weather = weather
        self.ice_proba = ice_proba
        self.norm_proba = norm_proba
        self.tree_fall_proba = tree_fall_proba
        self.fire_proba = fire_proba
    def __str__(self):
        return "Гололед:{0}, Норма:{1}, Падение деревьев:{2}, Пожар:{3}".format(self.ice_proba, self.norm_proba, self.tree_fall_proba, self.fire_proba)

class AccidentPredictor:
    api_key = '14a1414a-b8b2-4068-99d7-0d874bcea125'
    def __init__(self):
        self.weatherPredictor = YaWeather(api_key=self.api_key)
        self.classifier = Classifier()

    def get_accident(self, temp, windspeed, proba):
        w = Weather(None)
        w.temp = temp
        w.windspeed = windspeed
        return AccidentPredictionData(w, proba[0], proba[1], proba[2], proba[3])

    def predict(self, coord):
        responce = self.weatherPredictor.forecast(coord)
        weather = Weather(responce)
        proba = self.classifier.predict_accident(weather.get_data())[0]
        return AccidentPredictionData(weather, proba[0], proba[1], proba[2], proba[3])

    def predict_by_id(self, id):
        coords = {id: utils.CITY_TO_COORDS[id]}
        result = {}
        for city, coord in coords.items():
        #for city, coord in coords.items():
            try:
                res = self.predict(coord)
                result[city] = res
            except:
                pass
        print(result.keys())
        return result


    def predict_all(self):
        result = {}
        # coords = {'RU-KDA': yaweather.cities.Russia.Krasnodar,
        #          'RU-SVE': yaweather.cities.Russia.Yekaterinburg}
        for city, coord in utils.CITY_TO_COORDS.items():
        #for city, coord in coords.items():
            try:
                res = self.predict(coord)
                result[city] = res
            except:
                pass
        print(result.keys())
        return result