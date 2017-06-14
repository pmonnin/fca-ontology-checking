import json

__author__ = "Pierre Monnin"


class StatisticsSaver:
    def __init__(self):
        pass

    @staticmethod
    def save_statistics(statistics, file):
        with open(file, 'w') as file:
            json.dump(statistics, file)
