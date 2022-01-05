import datetime
import requests
from pprint import pprint
from config import OPEN_WEATHER_TOKEN as weather_token


def get_weather(city, weather_token):

    #словарь 'состояние погоды + эмоджи':
    code_to_smile = {
        "Clear": "Ясно  \U00002600",
        "Clouds": "Облачно  \U00002601",
        "Rain": "Дождь  \U00002614",
        "Drizzle": "Мелкий дождь    \U00002602",
        "Thunderstorm": "Гроза  \U000026A1",
        "Snow": "Снег   \U0001F328",
        "Mist": "Туман  \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"                #ссылка из current weather data
        )
        data = r.json()
        pprint(data)

        city = data['name']                                                 #название города из ответа
        curr_weather = data['main']['temp']                      #забираем температуру

        weather_description = data['weather'][0]['main']
        #если значение погоды совпадает с ключом словаря, то выводим 'значение + эмоджи':
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Осторожно посмотри в окно, не пойму что там за погода!"
       
        humidity = data['main']['humidity']                        #забираем влажность
        pressure = data['main']['pressure']                       #забираем давление
        wind = data['wind']['speed']                                   #скорость ветра
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])           #время рассвета
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])              #время заката
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])                         #продолжительность светового дня

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе: {city}\nТемпература: {curr_weather}°C {wd}\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                f"Продолжительность светового дня: {length_of_the_day}\n"
                f"Хорошего Вам дня!"
                )


    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите название города: ")
    get_weather(city, weather_token)


if __name__ == '__main__':
    main()