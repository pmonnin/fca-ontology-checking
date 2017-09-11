import sys

from core.lod.Ontology import Ontology

__author__ = "Pierre Monnin"


class Lattice:
    def __init__(self, concepts, objects, attributes, parents, children, ontology_classes=None):
        self._concepts = concepts
        self._objects = objects
        self._attributes = attributes
        self._parents = parents
        self._children = children
        self._ontology_classes = ontology_classes

        for i in range(0, len(self._concepts)):
            if len(self._parents[i]) == 0:
                self._top = i

            if len(self._children[i]) == 0:
                self._bottom = i

    def get_top_index(self):
        return self._top

    def get_bottom_index(self):
        return self._bottom

    def get_parents(self, concept_index):
        return self._parents[concept_index].copy()

    def get_children(self, concept_index):
        return self._children[concept_index].copy()

    def get_objects(self):
        return self._objects.copy()

    def get_attributes(self):
        return self._attributes.copy()

    def get_ontology_classes(self):
        return self._ontology_classes.copy()

    def get_concepts(self):
        return self._concepts.copy()

    def get_arcs_count(self):
        ret_val = 0
        for i in self._parents:
            ret_val += len(i)
        return ret_val

    def get_empty_annotations_count(self):
        ret_val = 0

        for c in self._concepts:
            if len(c["annotation-r"]) == 0:
                ret_val += 1

        return ret_val

    def annotate(self, classes_per_objects, ontology):
        self._ontology_classes = ontology.get_classes()

        for i, c in enumerate(self._concepts):
            sys.stdout.write("\rAnnotating concepts %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            c["annotation-r"] = set()
            if len(c["extent"]) != 0:
                c["annotation-r"] = set(classes_per_objects[c["extent"][0]])

                for j in range(1, len(c["extent"])):
                    c["annotation-r"] = c["annotation-r"] & set(classes_per_objects[c["extent"][j]])

        print("\rAnnotating concepts 100 %\t\t")

        reduced_annotations = []
        for i, c in enumerate(self._concepts):
            sys.stdout.write("\rComputing reduced notation of concepts annotations %i %%\t\t" %
                             (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            reduced_annotations.append(c["annotation-r"].copy())
            for p in self._parents[i]:
                reduced_annotations[i] -= self._concepts[p]["annotation-r"]

        print("\rComputing reduced notation of concepts annotations 100 %\t\t")

        for i, c in enumerate(self._concepts):
            sys.stdout.write("\rSaving reduced notation of concepts annotations %i %%\t\t" %
                             (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()
            c["annotation-r"] = list(reduced_annotations[i])

        print("\rSaving reduced notation of concepts annotations 100 %\t\t")

    def reduce_to_annotated_concepts(self):
        parents = []
        children = []
        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rPreparing lattice reduction %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            current_parents = {}
            for parent in self._parents[i]:
                current_parents[parent] = True

            current_children = {}
            for child in self._children[i]:
                current_children[child] = True

            parents.append(current_parents)
            children.append(current_children)

        print("\rPreparing lattice reduction 100 %\t\t")

        for i, c in enumerate(self._concepts):
            sys.stdout.write("\rReducing lattice to annotated concepts %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            if len(c["annotation-r"]) == 0:
                for parent in parents[i]:
                    del(children[parent][i])

                    for child in children[i]:
                        children[parent][child] = True
                        parents[child][parent] = True

                for child in children[i]:
                    del(parents[child][i])

                parents[i] = {}
                children[i] = {}

        print("\rReducing lattice to annotated concepts 100 %\t\t")

        for i in range(0, len(self._concepts)):
            sys.stdout.write("\rSaving new concepts subsumptions %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            self._parents[i] = list(parents[i].keys())
            self._children[i] = list(children[i].keys())

        print("\rSaving new concepts subsumptions 100 %\t\t")

        # TODO Useless concepts could be deleted to save space

    def get_ontology_from_annotations(self):
        index_to_class = self._ontology_classes
        class_to_index = {}
        class_parents = []
        class_children = []

        for i, c in enumerate(index_to_class):
            class_to_index[c] = i
            class_parents.append({})
            class_children.append({})

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rExtracting ontology from annotated lattice %i %%\t\t" %
                             (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            if len(concept["annotation-r"]) != 0:
                for p in self._parents[i]:
                    for ontology_class_parent in self._concepts[p]["annotation-r"]:
                        for ontology_class in concept["annotation-r"]:
                            class_parents[ontology_class][ontology_class_parent] = True
                            class_children[ontology_class_parent][ontology_class] = True

        print("\rExtracting ontology from annotated lattice 100 %\t\t")

        for i in range(0, len(index_to_class)):
            class_parents[i] = list(class_parents[i].keys())
            class_children[i] = list(class_children[i].keys())

        return Ontology(class_to_index, index_to_class, class_parents, class_children)
