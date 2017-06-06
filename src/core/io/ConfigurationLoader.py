import json

__author__ = "Pierre Monnin"


class ConfigurationLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_configuration(configuration_file_path):
        with open(configuration_file_path, encoding='utf-8') as configuration_file:
            return json.loads(configuration_file.read())

    @staticmethod
    def load_n_check_configuration(configuration_file_path, expected_fields):
        conf = ConfigurationLoader.load_configuration(configuration_file_path)

        missing_fields = []
        for field in expected_fields:
            if field not in conf:
                missing_fields.append(field)

        if len(missing_fields) != 0:
            raise KeyError("Missing fields in configuration file: " + str(missing_fields))

        return conf
