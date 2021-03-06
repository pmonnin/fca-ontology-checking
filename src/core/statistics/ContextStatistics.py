__author__ = "Pierre Monnin"


class ContextStatistics:
    def __init__(self):
        pass

    @staticmethod
    def compute_2d_context_statistics(context):
        statistics = {"objects-number": len(context), "relations-number": 0}

        attributes = []
        for obj in context:
            for att in context[obj]:
                if att not in attributes:
                    attributes.append(att)
            statistics["relations-number"] += len(context[obj])

        statistics["attributes-number"] = len(attributes)
        return statistics

    @staticmethod
    def compute_3d_context_statistics(context):
        statistics = {"objects-number": len(context), "relations-number": 0}

        attributes = []
        conditions = []
        hidden_objects = {}

        for obj in context.keys():
            if len(context[obj].keys()) == 0:
                hidden_objects[obj] = True

            for attribute in context[obj].keys():
                if attribute not in attributes:
                    attributes.append(attribute)

                if len(context[obj][attribute]) == 0:
                    hidden_objects[obj] = True

                for condition in context[obj][attribute]:
                    if condition not in conditions:
                        conditions.append(condition)

                statistics["relations-number"] += len(context[obj][attribute])

        statistics["attributes-number"] = len(attributes)
        statistics["conditions-number"] = len(conditions)
        statistics["hidden-objects-count"] = len(hidden_objects)
        return statistics
