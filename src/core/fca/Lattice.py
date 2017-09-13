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

    def get_ontology_from_mixed_intents(self, ontology, ontology_base_uri):
        # Concepts additional information
        ontological_intents = []
        reduced_ontological_intents = []
        concepts_parents = []
        concepts_children = []

        # Ontology information
        index_to_class = ontology.get_classes()
        class_to_index = {}
        class_parents = []
        class_children = []
        for i, ontology_class in enumerate(index_to_class):
            class_to_index[ontology_class] = i
            class_parents.append({})
            class_children.append({})

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rComputing ontological intent %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            ontological_intents.append(set())

            for a in concept["intent"]:
                if self._attributes[a].startswith(ontology_base_uri):
                    ontological_intents[i].add(self._attributes[a])

            concepts_parents.append({})
            concepts_children.append({})
            for parent in self._parents[i]:
                concepts_parents[i][parent] = True
            for child in self._children[i]:
                concepts_children[i][child] = True

        print("\rComputing ontological intent 100 %\t\t")

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rComputing reduced ontological intent %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            reduced_ontological_intents.append(ontological_intents[i].copy())

            for parent in concepts_parents[i]:
                reduced_ontological_intents[i] -= ontological_intents[parent]

        print("\rComputing reduced ontological intent 100 %\t\t")

        for i, c in enumerate(self._concepts):
            sys.stdout.write("\rReducing lattice to ontological intent %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            if len(reduced_ontological_intents[i]) == 0:
                for parent in concepts_parents[i]:
                    del(concepts_children[parent][i])

                    for child in concepts_children[i]:
                        concepts_children[parent][child] = True
                        concepts_parents[child][parent] = True

                for child in concepts_children[i]:
                    del(concepts_parents[child][i])

                concepts_parents[i] = {}
                concepts_children[i] = {}

        print("\rReducing lattice to ontological intent 100 %\t\t")

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rExtracting ontology from ontological intents of lattice %i %%\t\t" %
                             (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            if len(reduced_ontological_intents[i]) != 0:
                for parent in concepts_parents[i]:
                    for ontology_class in reduced_ontological_intents[i]:
                        for ontology_class_parent in reduced_ontological_intents[parent]:
                            if ontology_class in class_to_index and ontology_class_parent in class_to_index:
                                class_parents[class_to_index[ontology_class]][class_to_index[ontology_class_parent]] = \
                                    True
                                class_children[class_to_index[ontology_class_parent]][class_to_index[ontology_class]] \
                                    = True

        print("\rExtracting ontology from ontological intents of lattice 100 %\t\t")

        for i in range(0, len(class_parents)):
            class_parents[i] = list(class_parents[i].keys())
            class_children[i] = list(class_children[i].keys())

        return Ontology(class_to_index, index_to_class, class_parents, class_children)

    def get_ontology_from_projection_lattice_intents(self, ontology):
        # Ontology information
        index_to_class = ontology.get_classes()
        class_to_index = {}
        class_parents = []
        class_children = []
        for i, ontology_class in enumerate(index_to_class):
            class_to_index[ontology_class] = i
            class_parents.append({})
            class_children.append({})

        # Concepts additional information
        reduced_intents = []
        concepts_parents = []
        concepts_children = []

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rComputing reduced intents %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            reduced_intents.append(set(concept["intent"]))
            concepts_parents.append({})
            concepts_children.append({})

            for parent in self._parents[i]:
                concepts_parents[i][parent] = True
                reduced_intents[i] -= set(self._concepts[parent]["intent"])

            for child in self._children[i]:
                concepts_children[i][child] = True

        print("\rComputing reduced intents 100 %\t\t")

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rReducing lattice %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            if len(reduced_intents[i]) == 0:
                for parent in concepts_parents[i]:
                    del(concepts_children[parent][i])

                    for child in concepts_children[i]:
                        concepts_parents[child][parent] = True
                        concepts_children[parent][child] = True

                for child in concepts_children[i]:
                    del(concepts_parents[child][i])

                concepts_parents[i] = {}
                concepts_children[i] = {}

        print("\rReducing lattice 100 %\t\t")

        for i, concept in enumerate(self._concepts):
            sys.stdout.write("\rExtracting ontology from lattice %i %%\t\t" % (i * 100.0 / len(self._concepts)))
            sys.stdout.flush()

            # Length of extent should be > 0 otherwise there is no triconcept corresponding to this projection
            if len(concept["extent"]) != 0 and len(reduced_intents[i]) != 0:
                for parent in concepts_parents[i]:
                    for ontology_class_index in reduced_intents[i]:
                        for ontology_class_parent_index in reduced_intents[parent]:
                            ontology_class = self._attributes[ontology_class_index]
                            ontology_class_parent = self._attributes[ontology_class_parent_index]

                            if ontology_class in class_to_index and ontology_class_parent in class_to_index:
                                class_index = class_to_index[ontology_class]
                                parent_index = class_to_index[ontology_class_parent]

                                class_parents[class_index][parent_index] = True
                                class_children[parent_index][class_index] = True
                            else:
                                print("Error: classes not found: " + ontology_class + " " + ontology_class_parent)

        print("\rExtracting ontology from lattice 100 %\t\t")

        for i in range(0, len(class_parents)):
            class_parents[i] = list(class_parents[i].keys())
            class_children[i] = list(class_children[i].keys())

        return Ontology(class_to_index, index_to_class, class_parents, class_children)
