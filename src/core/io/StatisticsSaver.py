import json

__author__ = "Pierre Monnin"


class StatisticsSaver:
    def __init__(self):
        pass

    @staticmethod
    def save_statistics(statistics, file_path):
        with open(file_path, 'w') as file:
            json.dump(statistics, file, indent=4)
