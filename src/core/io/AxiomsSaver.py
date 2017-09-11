import csv

__author__ = "Pierre Monnin"


class AxiomsSaver:
    def __init__(self):
        pass

    @staticmethod
    def save_axioms(axioms, file_path):
        with open(file_path, 'w', encoding='utf-8') as output:
            csv_writer = csv.writer(output)
            csv_writer.writerow(['Bottom', 'Top', 'Type'])

            for a in axioms:
                csv_writer.writerow([a[0], a[1], a[2]])
