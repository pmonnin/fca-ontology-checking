__author__ = "Pierre Monnin"


class BinaryContextStatistics:
    def __init__(self):
        pass

    @staticmethod
    def compute_statistics(context):
        statistics = {"objects-number": len(context), "attributes-number": 0, "attributes-per-object": 0}

        attributes = []
        for obj in context:
            for att in context[obj]:
                if att not in attributes:
                    attributes.append(att)
            statistics["attributes-per-object"] += len(context[obj])

        statistics["attributes-per-object"] /= float(len(context))
        statistics["attributes-number"] = len(attributes)
        return statistics
