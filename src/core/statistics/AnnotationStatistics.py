__author__ = "Pierre Monnin"


class AnnotationStatistics:
    def __init__(self):
        pass

    @staticmethod
    def compute_statistics(lattice):
        statistics = {'empty-annotations': lattice.get_number_of_empty_annotations()}
        return statistics
