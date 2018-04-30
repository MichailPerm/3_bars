import math
import argparse
import json
import sys


def create_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    return parser.parse_args()


def load_data(filepath):
    with open(filepath, 'r') as file:
        dict_content = json.load(file)
        return dict_content['features']


def get_biggest_bar(dicts_list):
    return max(
        dicts_list,
        key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(dicts_list):
    return min(
        dicts_list,
        key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_closest_bar(dicts_list, longitude, latitude):
    return min(dicts_list, key=lambda x: math.sqrt(
        ((float(longitude) - x['geometry']['coordinates'][0]) ** 2) + (
                (float(latitude) - x['geometry']['coordinates'][1]) ** 2)))


if __name__ == '__main__':
    args = create_args_parser()
    try:
        dicts_list = load_data(args.filepath)
    except json.decoder.JSONDecodeError:
        print('Файл {} не содержит данных json.'.format(args.filepath))
    except IOError:
        print('Невозможно прочитать данные {}.'.format(args.filepath))
    else:
        if not dicts_list:
            sys.exit('Программа завершила работу из-за отсутствия данных json.')
        else:
            the_biggest_bar = get_biggest_bar(dicts_list)
            the_smallest_bar = get_smallest_bar(dicts_list)
            longitude = input('Введите долготу: ')
            latitude = input('Введите широту: ')
            try:
                float_longitude = float(longitude)
            except (ValueError, NameError):
                sys.exit('Программа завершила работу из-за некорректно введенной долготы')
            try:
                float_latitude = float(latitude)
            except (ValueError, NameError):
                sys.exit('Программа завершила работу из-за некорректно введенной широты')
            the_closest_bar = get_closest_bar(dicts_list, longitude, latitude)
            print('Самый маленький бар - {}'.format(
                the_smallest_bar['properties']['Attributes']['Name']))
            print('Самый большой бар - {}'.format(
                the_biggest_bar['properties']['Attributes']['Name']))
            print('Самый близкий бар - {}'.format(
                the_closest_bar['properties']['Attributes']['Name']))
