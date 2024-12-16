import json
import requests

from datetime import datetime, timedelta

# These are the coordinate of central London. Please change at your convenience
from wafl.exceptions import CloseConversation

_db_filename = "db.json"

def close_conversation():
    raise CloseConversation()


def check_today_weather():
    return check_weather_lat_long(day_offset=0)


def check_tomorrow_weather():
    today = datetime.now()
    return check_weather_lat_long(day_offset=1)


def check_weather_lat_long(day_offset):
    secrets = json.load(open("secrets.json"))
    result = requests.get(
        f"https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": secrets["latitude"],
            "longitude": secrets["longitude"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
        }
    )

    data = result.json()
    if "daily" not in data:
        return "There is a connection error to the weather API. Please try later"

    to_say = ""
    temperature_min = data["daily"]["temperature_2m_min"][day_offset]
    temperature_max = data["daily"]["temperature_2m_max"][day_offset]
    to_say += f"The temperature will be between {temperature_min} and {temperature_max} degrees.\n"
    precipitation = data["daily"]["precipitation_sum"][day_offset]
    to_say += f"The precipitation probability is {precipitation} %.\n"
    return to_say


def get_time():
    return datetime.now().strftime("%H %M")


def get_date():
    return datetime.now().strftime("%Y %m %d")


def get_day():
    return datetime.now().strftime("%A")



def add_to_shopping_list(list_of_items_to_add):
    db = json.load(open(_db_filename))
    for item in list_of_items_to_add:
        if item not in db["shopping_list"]:
            db["shopping_list"].append(item)

    json.dump(db, open(_db_filename, "w"))

    return "Item added"


def remove_shopping_list(list_of_items_to_remove):
    db = json.load(open(_db_filename))
    for item in list_of_items_to_remove:
        if item in db["shopping_list"]:
            db["shopping_list"].remove(item)

    json.dump(db, open(_db_filename, "w"))

    return "Item removed"


def get_shopping_list():
    db = json.load(open(_db_filename))
    if db["shopping_list"] == []:
        return "nothing"

    return ", ".join(db["shopping_list"])


def write_to_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)

    return f"File {filename} saved"
