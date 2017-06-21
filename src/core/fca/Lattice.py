import bisect

__author__ = "Pierre Monnin"


class Lattice:
    def __init__(self, sofia_lattice_json):
        self._top = sofia_lattice_json[0]["Top"][0]
        self._bottom = sofia_lattice_json[0]["Bottom"][0]
        self._objects = []
        self._attributes = []
        self._concepts = []
        self._parents = []
        self._children = []

        # Concepts
        for c in sofia_lattice_json[1]["Nodes"]:
            concept = {"extent": [], "intent": []}

            for i in range(0, len(c["Ext"]["Inds"])):
                o = c["Ext"]["Inds"][i]
                concept["extent"].append(o)
                Lattice.__extend_list(self._objects, o, c["Ext"]["Names"][i], "")

            if c["Int"] != "BOTTOM":
                for i in range(0, len(c["Int"]["Inds"])):
                    a = c["Int"]["Inds"][i]
                    concept["intent"].append(a)
                    Lattice.__extend_list(self._attributes, a, c["Int"]["Names"][i], "")

            self._concepts.append(concept)

        # Arcs
        for i in range(0, len(self._concepts)):
            self._parents.append([])
            self._children.append([])

        for a in sofia_lattice_json[2]["Arcs"]:
            bisect.insort_left(self._children[a["S"]], a["D"])
            bisect.insort_left(self._parents[a["D"]], a["S"])

    def get_top_index(self):
        return self._top

    def get_children(self, concept_index):
        return list(self._children[concept_index])

    @staticmethod
    def __extend_list(l, index, element, default_element):
        while index >= len(l):
            l.append(default_element)

        l[index] = element
