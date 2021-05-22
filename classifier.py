import joblib
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
        'e': 180,
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
        self.lon = responce.info.lon
        self.lat = responce.info.lat
        self.temp = responce.fact.temp
        self.winddir = get_winddir(responce.fact.wind_dir)
        self.windspeed = responce.fact.wind_speed

        forecast = responce.forecasts[0]
        for f in responce.forecasts:
            print(f.date)
        self.precipitation = forecast.prec_mm if forecast.prec_mm is not None else 0
        self.snowstorm = check_condition_type(responce.fact.phenom_condition,
                                              [PhenomCondition.drifting_snow, PhenomCondition.blowing_snow, PhenomCondition.ice_pellets])
        self.mist = check_condition_type(responce.fact.phenom_condition, [PhenomCondition.fog, PhenomCondition.mist, PhenomCondition.smoke])
        self.hail = check_condition_type(responce.fact.prec_type, [PrecipitationType.hail])
        self.glaze_ice = check_condition_type(responce.fact.phenom_condition, [PhenomCondition.ice_pellets])
        self.blast = 0
        self.squall = 0
        self.storm_rainfall = 0
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
        print(self.classifier.classes_)
        return self.classifier.predict_proba(data)*100


class AccidentPredictor:
    api_key = '14a1414a-b8b2-4068-99d7-0d874bcea125'
    def __init__(self):
        self.weatherPredictor = YaWeather(api_key=self.api_key)
        self.classifier = Classifier()
    def predict(self, coord):
        responce = self.weatherPredictor.forecast(coord)
        weather = Weather(responce).get_data()
        return self.classifier.predict_accident(weather)
