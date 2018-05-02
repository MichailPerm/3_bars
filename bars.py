import json


def load_data(filepath):
    f = open(filepath, 'r')
    json_data = json.load(f, encoding='utf8')
    f.close()
    return json_data


def get_biggest_bar(data):
    pass


def get_smallest_bar(data):
    pass


def get_closest_bar(data, longitude, latitude):
    pass


if __name__ == '__main__':
    data = load_data('bars.json')
    import pdb; pdb.set_trace()
