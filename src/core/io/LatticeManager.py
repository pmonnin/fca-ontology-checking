import bisect
import json

from core.fca.Lattice import Lattice

__author__ = "Pierre Monnin"


class LatticeManager:
    def __init__(self):
        pass

    @staticmethod
    def load_2d_sofia_lattice(lattice_path):
        with open(lattice_path, encoding='utf-8') as lattice_file:
            sofia_lattice_json = json.loads(lattice_file.read())

            objects = []
            attributes = []
            concepts = []
            parents = []
            children = []

            # Concepts
            for c in sofia_lattice_json[1]["Nodes"]:
                concept = {"extent": [], "intent": []}

                for i in range(0, len(c["Ext"]["Inds"])):
                    o = c["Ext"]["Inds"][i]
                    concept["extent"].append(o)
                    LatticeManager.__extend_list(objects, o, c["Ext"]["Names"][i], "")

                if c["Int"] != "BOTTOM":
                    for i in range(0, len(c["Int"]["Inds"])):
                        a = c["Int"]["Inds"][i]
                        concept["intent"].append(a)
                        LatticeManager.__extend_list(attributes, a, c["Int"]["Names"][i], "")

                concepts.append(concept)

            # Arcs
            for i in range(0, len(concepts)):
                parents.append([])
                children.append([])

            for a in sofia_lattice_json[2]["Arcs"]:
                bisect.insort_left(children[a["S"]], a["D"])
                bisect.insort_left(parents[a["D"]], a["S"])

            return Lattice(concepts, objects, attributes, parents, children)

    @staticmethod
    def __extend_list(l, index, element, default_element):
        while index >= len(l):
            l.append(default_element)

        l[index] = element

    @staticmethod
    def save_annotated_lattice(file_path, lattice):
        with open(file_path, 'w', encoding='utf-8') as file:
            json_lattice = {"objects": lattice.get_objects(), "attributes": lattice.get_attributes(),
                            "ontology_classes": lattice.get_ontology_classes(), "concepts": [], "parents": [],
                            "children": []}

            for i, c in enumerate(lattice.get_concepts()):
                if i != lattice.get_bottom_index():
                    json_lattice["concepts"].append(c)
                else:
                    json_lattice["concepts"].append({"extent": c["extent"], "intent": "BOTTOM",
                                                     "annotation-r": c["annotation-r"]})
                json_lattice["parents"].append(lattice.get_parents(i))
                json_lattice["children"].append(lattice.get_children(i))

            json.dump(json_lattice, file)
