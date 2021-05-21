import pandas as pd
import re
from datetime import datetime


class WeatherCenterParser:
    filename = 'Погода_центры_2020.xls'
    subject = 'name'
    date = 'datetime_d'
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self):
        self.df = pd.read_excel(self.filename)

    def get_subjects_by_date(self, date):
        date_time1 = datetime(date.year, date.month, date.day, 12, 0, 0)
        dates = self.df[self.date].apply(lambda x: datetime.strptime(x, self.datetime_format))
        cond = (dates == date_time1)
        return self.df.loc[cond]


class AccidentsCauses2020Parser:
    filename = 'Аварии_погода_САЦ_2020.xls'
    subject = 'Субъект РФ2'
    date = 'Дата (местное время)'

    def __init__(self):
        self.df = pd.read_excel(self.filename)

class AccidentWeather2020Parser:
    filename = 'Аварии_погода_САЦ_2020.xls'
    subject = 'Субъект РФ'
    date = 'Дата'
    cause = 'Причина'
    description = 'Подробности'
    type = 'Тип объекта'

    def __init__(self):
        self.df = pd.read_excel(self.filename)

    def get_subjects_by_date(self, date):
        dates = self.df[self.date].apply(lambda x: x.date())
        cond = (dates == date)
        return self.df.loc[cond]

