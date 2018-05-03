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


def get_biggest_bar(bars):
    return max(
        bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars):
    return min(
        bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars, longitude, latitude):
    return min(bars, key=lambda x: math.sqrt(
        ((longitude - x['geometry']['coordinates'][0]) ** 2) + (
         (latitude - x['geometry']['coordinates'][1]) ** 2)))


def get_coordinate_value(coordinate_name):
    coordinate_value = input('{}: '.format(coordinate_name))
    return check_coordinate_value(
        coordinate_value)


def check_coordinate_value(coordinate_value):
    try:
        float_coordinate_value = float(coordinate_value)
        return float_coordinate_value
    except (ValueError, TypeError):
        return None


def print_bars(the_biggest_bar, the_smallest_bar, the_closest_bar):
    print('Самый маленький бар - {}'.format(
        the_smallest_bar['properties']['Attributes']['Name']))
    print('Самый большой бар - {}'.format(
        the_biggest_bar['properties']['Attributes']['Name']))
    print('Самый близкий бар - {}'.format(
        the_closest_bar['properties']['Attributes']['Name']))


def get_bars(bars):
    the_biggest_bar = get_biggest_bar(bars)
    the_smallest_bar = get_smallest_bar(bars)
    longitude = get_coordinate_value('Долгота')
    if longitude is None:
        sys.exit(
            'Долгота введена неверно. Программа завершила работу.')
    latitude = get_coordinate_value('Широта')
    if latitude is None:
        sys.exit(
            'Широта введена неверно. Программа завершила работу.')
    the_closest_bar = get_closest_bar(bars, longitude, latitude)
    print_bars(the_biggest_bar, the_smallest_bar, the_closest_bar)


if __name__ == '__main__':
    args = create_args_parser()
    try:
        bars = load_data(args.filepath)
    except json.decoder.JSONDecodeError:
        sys.exit('Файл {} не содержит данных json.'.format(args.filepath))
    except IOError:
        sys.exit('Невозможно прочитать данные {}.'.format(args.filepath))
    if not bars:
        sys.exit('Программа завершила работу из-за отсутствия данных json.')
    get_bars(bars)
