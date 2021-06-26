import argparse

from models import Radar

parser = argparse.ArgumentParser(
    description='Reveals possible locations of invaders on given radar sample')
parser.add_argument('-a', '--accuracy', type=int, required=False, default=85,
                    help='Accuracy of invader detection between 0 and 100.')
# TODO maybe between 0-1? but this is more user friendly
parser.add_argument('-f', '--file-path', type=str, required=False, default='../README.md',
                    help='Relative path of the input file.')


def clean_accuracy(accuracy: int) -> float:
    return float(accuracy) / 100


def clean_file_name(file_path: str) -> str:
    # TODO handle either way? relative or full path
    return file_path


if __name__ == '__main__':
    args = parser.parse_args()
    accuracy = clean_accuracy(args.accuracy)
    file_path = clean_file_name(args.file_path)

    radar = Radar(accuracy)
    radar.init_from_file(file_path)

    radar.scan()
    radar.dump_to_file(file_path)
    a = 5
