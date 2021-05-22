
from model import Model
import datetime


if __name__ == "__main__":
    model = Model()
    datas = model.get_subjects_by_date(datetime.date(2020, 7, 7))
    for data in datas:
        print(data)
