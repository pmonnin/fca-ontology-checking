import json

__author__ = "Pierre Monnin"


class SofiaBinaryContextManager:
    def __init__(self):
        pass

    @staticmethod
    def save_context(context, file):
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
