import requests
import datetime
from config import open_weather_token, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from logger import log

tg_bot = Bot(token= tg_bot_token)
dp = Dispatcher(tg_bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет. Напиши мне название города')

@dp.message_handler()
async def get_weather(message: types.Message):
    log(message)  
    code_to_smile = {
        'Clear': 'Ясно \U00002600', 
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F328'
    }

    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric')
        data = r.json()
        
        city = data['name']
        cur_weather = data['main']['temp']
        
        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не понимаю, что там за аномалия'
            
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_time - sunrise_time
        
        await message.reply(f'***{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}***\n'
              f'Погода в городе: {city}\nТемпература: {cur_weather}С° {wd}\n'
              f'Влажность: {humidity}%\nСкорость ветра: {wind} м/с\nРассвет: {sunrise_time.strftime("%d-%m-%Y %H:%M")}\n'
              f'Закат: {sunset_time.strftime("%d-%m-%Y %H:%M")}\nСветовой день: {length_of_the_day}')
        
        
    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')
        


if __name__ == '__main__':
    executor.start_polling(dp)