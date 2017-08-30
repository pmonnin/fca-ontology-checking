import json

__author__ = "Pierre Monnin"


class ContextManager:
    def __init__(self):
        pass

    @staticmethod
    def save_2d_context_for_sofia(context, file):
        data = [
            {
                "ObjNames": [],
                "Params": {
                    "AttrNames": []
                }
            },
            {
                "Count": len(context),
                "Data": []
            }
        ]

        for obj in context:
            data[0]["ObjNames"].append(obj)
            data[1]["Data"].append({"Count": len(context[obj]), "Inds": []})
            inds = []

            for attr in context[obj]:
                if attr not in data[0]["Params"]["AttrNames"]:
                    data[0]["Params"]["AttrNames"].append(attr)

                inds.append(data[0]["Params"]["AttrNames"].index(attr))

            # Quick-sort of inds

            data[1]["Data"][len(data[1]["Data"]) - 1]["Inds"] = sorted(inds)

        with open(file, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def save_3d_context_for_data_peeler(context, file):
        with open(file, 'w') as file:
            for obj in context.keys():
                for attribute in context[obj].keys():
                    for condition in context[obj][attribute]:
                        file.write(obj + " " + attribute + " " + condition + "\n")
