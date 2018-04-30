import requests
import math


LONGITUDE = 0
LATITUDE = 0


def load_data():
    json_data = requests.get('https://apidata.mos.ru/v1/features/1796',
                             params={'api_key': '2df488852a3e23b21e09a739eab2977a'})\
        .json()
    return json_data['features']


def get_biggest_bar(json_data):
    return max(json_data, key=lambda x: x['properties']['Attributes']['SeatsCount'])\
        ['properties']['Attributes']['Name']


def get_smallest_bar(json_data):
    return min(json_data, key=lambda x: x['properties']['Attributes']['SeatsCount'])\
        ['properties']['Attributes']['Name']


def get_closest_bar(json_data):
    return min(json_data, key=lambda x: math.sqrt(
        ((float(LONGITUDE) - x['geometry']['coordinates'][0]) ** 2) + (
                (float(LATITUDE) - x['geometry']['coordinates'][1]) ** 2)))\
        ['properties']['Attributes']['Name']


if __name__ == '__main__':
    json_data = load_data()
    the_biggest_bar = get_biggest_bar(json_data)
    the_smallest_bar = get_smallest_bar(json_data)
    LONGITUDE = input('Введите долготу: ')
    LATITUDE = input('Введите широту: ')
    the_closest_bar = get_closest_bar(json_data)
    print('Самый маленький бар - %s\n' % the_smallest_bar)
    print('Самый большой бар - %s\n' % the_biggest_bar)
    print('Самый близкий бар - %s\n' % the_closest_bar)
