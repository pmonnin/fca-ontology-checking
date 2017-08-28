import sys
import bisect

from queue import Queue
from core.fca.Lattice import Lattice
from core.lod.Ontology import Ontology

__author__ = "Pierre Monnin"


class AnnotatedLattice(Lattice):
    def __init__(self, lattice):
        self._ontology = None
        self._top = lattice._top
        self._bottom = lattice._bottom
        self._objects = list(lattice._objects)
        self._attributes = list(lattice._attributes)
        self._concepts = list(lattice._concepts)
        self._parents = list(lattice._parents)
        self._children = list(lattice._children)

        self._classes_per_concept = []
        for i in range(0, len(self._objects)):
            self._classes_per_concept.append([])

    def annotate(self, classes_per_object, ontology):
        self._ontology = ontology

        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rAnnotating concepts %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            temp_annotation = set()

            if len(self._concepts[i]["extent"]) != 0:
                temp_annotation = set(classes_per_object[self._concepts[i]["extent"][0]])

                for j in range(1, len(self._concepts[i]["extent"])):
                    temp_annotation = temp_annotation & set(classes_per_object[self._concepts[i]["extent"][j]])

            self._concepts[i]["annotation"] = []
            for j in temp_annotation:
                bisect.insort_left(self._concepts[i]["annotation"], j)

        print("\rAnnotating concepts 100 %\t\t")

    def reduce_annotation(self):
        reduced_annotations = []

        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rComputing concepts reduced annotations %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            temp_reduced_annotation = set(self._concepts[i]["annotation"])

            for j in self._parents[i]:
                temp_reduced_annotation = temp_reduced_annotation - set(self._concepts[j]["annotation"])

            reduced_annotations.append(temp_reduced_annotation)
        print("\rComputing concepts reduced annotations 100 %\t\t")

        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rSaving concepts reduced annotations %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            self._concepts[i]["annotation"] = []
            for j in reduced_annotations[i]:
                bisect.insort_left(self._concepts[i]["annotation"], j)

        print("\rSaving concepts reduced annotations 100 %\t\t")

    def reduce_to_closed_annotated_concepts(self):
        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rReducing lattice to closed annotated concepts %i %%\t\t" %
                             (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            if len(self._concepts[i]["annotation"]) == 0:
                for child in self._children[i]:
                    self._parents[child].remove(i)

                for child in self._children[i]:
                    for parent in self._parents[i]:
                        if parent not in self._parents[child]:
                            bisect.insort_left(self._parents[child], parent)
                            bisect.insort_left(self._children[parent], child)

                for parent in self._parents[i]:
                    self._children[parent].remove(i)

                self._children[i] = []
                self._parents[i] = []

        print("\rReducing lattice to closed annotated concepts 100 %\t\t")

        i = 0
        count = 0
        initial_length = len(self._concepts)
        while i < len(self._concepts):
            sys.stdout.write("\rRemoving useless concepts %i %%\t\t" % (count * 100.0 / initial_length))
            sys.stdout.flush()

            if len(self._concepts[i]["annotation"]) == 0:
                self._concepts.remove(self._concepts[i])
                del self._parents[i]
                del self._children[i]

                for j in range(0, len(self._concepts)):
                    for p_index in range(0, len(self._parents[j])):
                        if self._parents[j][p_index] >= i:
                            self._parents[j][p_index] -= 1

                    for c_index in range(0, len(self._children[j])):
                        if self._children[j][c_index] >= i:
                            self._children[j][c_index] -= 1

            else:
                i += 1

            count += 1

        print("\rRemoving useless concepts 100 %\t\t")

    def __compute_ancestors__(self, concept_index):
        ancestors = list(self._parents[concept_index])

        q = Queue()
        for parent in self._parents[concept_index]:
            q.put(parent)

        while not q.empty():
            c_id = q.get()

            for parent in self._parents[c_id]:
                if parent not in ancestors:
                    bisect.insort_left(ancestors, parent)
                    q.put(parent)

        return ancestors

    def get_number_of_empty_annotations(self):
        empty_ann = 0

        for i in self._concepts:
            if len(i["annotation"]) == 0:
                empty_ann += 1

        return empty_ann

    def get_ontology_schema_from_lattice(self):
        class_to_index = self._ontology._class_to_index
        index_to_class = self._ontology._index_to_class
        class_parents = []
        class_children = []

        for i in range(0, len(class_to_index)):
            class_parents.append([])
            class_children.append([])

        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rComputing ontology from lattice %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            for j in self._parents[i]:
                for c1 in self._concepts[i]["annotation"]:
                    for c2 in self._concepts[j]["annotation"]:
                        if c2 not in class_parents[c1]:
                            class_parents[c1].append(c2)
                            class_children[c2].append(c1)

        print("\rComputing ontology from lattice 100 %\t\t")
        return Ontology(class_to_index, index_to_class, class_parents, class_children)
