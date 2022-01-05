from aiogram.types import message
import requests
import datetime
from config import TOKEN_TELEBOT as tokenbot
from config import OPEN_WEATHER_TOKEN as token_weather
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tokenbot)
dp = Dispatcher(bot)


#бот даст ответ на команду "start"
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")

#вывод погоды в городе:
@dp.message_handler()
async def get_weather(message: types.Message):
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
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token_weather}&units=metric"                #ссылка из current weather data
        )
        data = r.json()

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

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе: {city}\nТемпература: {curr_weather}°C {wd}\n"
                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
                f"Продолжительность светового дня: {length_of_the_day}\n"
                f"***Хорошего Вам дня!***"
                )


    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")



if __name__ == '__main__':
    executor.start_polling(dp)                  #запуск бота