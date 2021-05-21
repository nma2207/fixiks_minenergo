import parsers
import utils

class WeatherData:
    def __init__(self, date, subject, temperature, wind_speed, event=None, description=None, type=None):
        self.date = date
        self.subject = subject
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.event = event
        self.description = description
        self.type = type
    def __str__(self):
        return "Weather Data [date:{0} subject:{1} event:{2} temp:{3}]".format(self.date, self.subject,self.event,self.temperature)

class Model:
    def __init__(self):
        self.weather_center_parser = parsers.WeatherCenterParser()
        self.accident_weather_parser = parsers.AccidentWeather2020Parser()

    def get_subjects_by_date(self, date):
        accidents = self.accident_weather_parser.get_subjects_by_date(date)
        weather = self.weather_center_parser.get_subjects_by_date(date)
        weather_datas = []

        for i in range(len(weather)):
            weather_data = weather.iloc[i]
            city_name = weather_data[self.weather_center_parser.subject]
            if city_name in utils.CITIES_TO_SUBJECTS:
                subject_name = utils.CITIES_TO_SUBJECTS[city_name]
                id = utils.CITIES_TO_ID[city_name]
                temperature = weather_data['temperature']
                wind_speed = weather_data['windspeedms']

                if sum(accidents[self.accident_weather_parser.subject] == subject_name)>0:
                    accident_by_subject = accidents[accidents[self.accident_weather_parser.subject] == subject_name]

                    for j in range(len(accident_by_subject)):
                        accident_data = accident_by_subject.iloc[j]
                        event = accident_data[self.accident_weather_parser.cause]
                        description = accident_data[self.accident_weather_parser.description]
                        type = accident_data[self.accident_weather_parser.type]
                        data = WeatherData(date, id, temperature, wind_speed, event, description, type)
                        weather_datas.append(data)

                else:
                    data = WeatherData(date, id, temperature, wind_speed)
                    weather_datas.append(data)

        return weather_datas
