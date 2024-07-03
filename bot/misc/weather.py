import datetime
import json
import re

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}


def weather_now(data):
    city = data["name"]
    cur_temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = round(data["main"]["pressure"] / 1.333)
    wind = data["wind"]["speed"]

    weather_description = data["weather"][0]["main"]

    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = "Посмотри в окно, я не понимаю, что там за погода..."

    return (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n" +
            f"Погода в городе: {city}\n" +
            f"Температура: {cur_temp}°C {wd}\n" +
            f"Влажность: {humidity}%\n" +
            f"Давление: {pressure} мм.рт.ст\n" +
            f"Ветер: {wind} м/с \n" +
            "Хорошего дня!")


def weather_5_days(data):
    dirct = {}
    for i in data['list']:
        time = i['dt_txt'].split()[1][:-3:]
        temp = round(i['main']['temp'])
        weather = code_to_smile[i['weather'][0]['main']]
        date = re.split("\\s|-", i['dt_txt'])
        date = date[2] + "." + date[1]
        if date in dirct:
            dirct[date][0].append(time)
            dirct[date][1].append(temp)
            dirct[date][2].append(weather)
        else:
            dirct[date] = [[time], [temp], [weather]]
    city = data["city"]["name"]

    s = f"Погода в городе {city}: \n" \
        "День\t| Темп |  Статус\n"
    for i in dirct:
        avg = round(sum(dirct[i][1]) / len(dirct[i][1]))
        unic = set(dirct[i][2])
        s += f'{i}\t| {avg}°C | {' и '.join(x for x in unic)}\n'
    weather_days(data, s)
    return s


def weather_days(data, strl):
    dirct = {}
    for i in data['list']:
        time = int(i['dt_txt'].split()[1][:-6:])
        temp = round(i['main']['temp'])
        feels_like = round(i['main']['feels_like'])
        pressure = round(i['main']['pressure'] / 1.333)
        weather = code_to_smile[i['weather'][0]['main']]
        wind = i["wind"]["speed"]

        date = re.split("\\s|-", i['dt_txt'])
        date = date[2] + "." + date[1]
        if date not in dirct:
            dirct[date] = {
                'night': {
                    'time': [],
                    'temp': [],
                    'feels_like': [],
                    'pressure': [],
                    'weather': [],
                    'wind': []
                },
                'morning': {
                    'time': [],
                    'temp': [],
                    'feels_like': [],
                    'pressure': [],
                    'weather': [],
                    'wind': []
                },
                'day': {
                    'time': [],
                    'temp': [],
                    'feels_like': [],
                    'pressure': [],
                    'weather': [],
                    'wind': []
                },
                'evening': {
                    'time': [],
                    'temp': [],
                    'feels_like': [],
                    'pressure': [],
                    'weather': [],
                    'wind': []
                }
            }
        if time < 6:
            period = 'night'
        elif time < 12:
            period = 'morning'
        elif time < 18:
            period = 'day'
        else:
            period = 'evening'

        dirct[date][period]['time'].append(time)
        dirct[date][period]['temp'].append(temp)
        dirct[date][period]['feels_like'].append(feels_like)
        dirct[date][period]['pressure'].append(pressure)
        dirct[date][period]['weather'].append(weather)
        dirct[date][period]['wind'].append(wind)
    dirct["All Days"] = strl
    save_weather(dirct, data)


def save_weather(dirct, data):
    with open(f'weather_{data["city"]["name"]}.json', 'w+') as outfile:
        json.dump(dirct, outfile, indent=4)
        outfile.close()


def weather_day(numday, city):
    with open(f'weather_{city}.json', 'r') as f:
        days = json.load(f)
    keys_list = list(days)
    if len(keys_list) == 7 and numday == 5:
        numday = 6
    day_key = keys_list[numday]
    data = days[day_key]

    if day_key == "All Days":
        return data
    # rows = []
    # for period, details in days[day_key].items():
    #     row = {
    #         "Period": period.capitalize(),
    #         "Time": format_range(details["time"]),
    #         "Temp": format_range(details["temp"]),
    #         "Feels Like": format_range(details["feels_like"]),
    #         "Pressure": format_range(details["pressure"]),
    #         "Weather": determine_weather(details["weather"]),
    #         "Wind": format_range(details["wind"])
    #     }
    #     rows.append(row)
    #
    # # Создаем DataFrame
    # df = pd.DataFrame(rows)
    #
    # # Транспонируем DataFrame
    # df_transposed = df.set_index('Period').transpose()
    #
    # return tabulate(df, headers='keys', tablefmt='grid')
    table = "Парам | Ночь | Утро | День | Вечер\n"
    parameters = ["time", "temp", "feels_like", "pressure", "weather", "wind"]
    param_rus = {"time": "Время", "temp": "Темп", "feels_like": "Ощущается", "pressure": "Давление",
                 "weather": "Погода", "wind": "Ветер"}
    for param in parameters:
        row = f"{param_rus[param]}"
        for period in ["night", "morning", "day", "evening"]:
            values = data[period][param]
            if values:
                try:
                    if values[0] == values[1]:
                        row += f" {values[0]} "
                    else:
                        row += f" {values[0]}-{values[1]} "
                except IndexError:
                    row += f" {values[0]}"
            else:
                row += f" - "
        table += row + "\n"

    return table

# def format_range(values):
#     if values[0] == values[1]:
#         return str(values[0])
#     else:
#         return " - ".join(map(str, values))
#
#
# def determine_weather(conditions):
#     if "Дождь ☔" in conditions:
#         return "Дождь ☔"
#     elif "Облачно ☁" in conditions:
#         return "Облачно ☁"
#     elif "Ясно ☀" in conditions:
#         return "Ясно ☀"
#     else:
#         return " - ".join(conditions)
