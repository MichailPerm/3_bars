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


def check_coordinate_value(coordinate_value):
    try:
        float_coordinate_value = float(coordinate_value)
        return float_coordinate_value
    except (ValueError, TypeError):
        return None


def print_bar(bar, msg):
    print(msg.format(bar['properties']['Attributes']['Name']))


def get_bars(bars, longitude, latitude):
    bars_result = {}
    bars_result['the_biggest_bar'] = get_biggest_bar(bars)
    bars_result['the_smallest_bar'] = get_smallest_bar(bars)
    if longitude is None or latitude is None:
        return None
    bars_result['the_closest_bar'] = get_closest_bar(bars, longitude, latitude)
    return bars_result


if __name__ == '__main__':
    args = create_args_parser()
    try:
        bars = load_data(args.filepath)
    except json.decoder.JSONDecodeError:
        sys.exit('Файл {} не содержит данных json.'.format(args.filepath))
    except IOError:
        sys.exit('Невозможно прочитать данные {}.'.format(args.filepath))
    longitude = check_coordinate_value(input('Долгота: '))
    latitude = check_coordinate_value(input('Широта: '))
    bars_result = get_bars(bars, longitude, latitude)
    if bars_result is None:
        sys.exit('Неверно заданы координаты. Программа завершила работу.')
    print_bar(bars_result['the_smallest_bar'], 'Самый маленький бар: {}')
    print_bar(bars_result['the_biggest_bar'], 'Самый большой бар - {}')
    print_bar(bars_result['the_closest_bar'], 'Самый близкий бар - {}')
