from classifier import AccidentPredictor
from yaweather.cities import Russia


if __name__ == "__main__":
    pred = AccidentPredictor()
    res = pred.predict(Russia.Moscow)
    print(res)
