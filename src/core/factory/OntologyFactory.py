import bisect
import sys

from core.lod.Ontology import Ontology

__author__ = "Pierre Monnin"


class OntologyFactory:
    def __init__(self, server_manager):
        self._server_manager = server_manager

    def build_ontology_from_lattice_objects(self, lattice, configuration):
        class_to_index = {}
        index_to_class = []
        class_parents = []
        class_children = []
        classes_per_object = []

        # Query the whole set of classes linked to the objects
        lattice_objects = lattice.get_objects()
        for i, o in enumerate(lattice_objects):
            classes_per_object.append([])
            sys.stdout.write("\rQuerying associated ontology classes %i %%\t\t" % (i * 100.0 / len(lattice_objects)))
            sys.stdout.flush()

            query = configuration["query-prefix"] + " select distinct ?class where { <" + o + "> " \
                + configuration["type-predicate"] + "/" + configuration["parent-predicate"] + "* ?class . " \
                + "FILTER(REGEX(STR(?class), \"" + configuration["ontology-base-uri"] + "\", \"i\")) . }"

            response = self._server_manager.query_server(query)

            for c in response["results"]["bindings"]:
                c_uri = c["class"]["value"]

                if c_uri not in class_to_index:
                    index_to_class.append(c_uri)
                    class_to_index[c_uri] = len(index_to_class) - 1

                bisect.insort_left(classes_per_object[i], class_to_index[c_uri])

        print("\rQuerying associated ontology classes 100 %\t\t")

        # Query the subsumption relations between classes
        for i in range(0, len(class_to_index)):
            class_parents.append([])
            class_children.append([])

        for i, c in enumerate(index_to_class):
            sys.stdout.write("\rQuerying ontology classes subsumptions %i %%\t\t" % (i * 100.0 / len(index_to_class)))
            sys.stdout.flush()

            query = configuration["query-prefix"] + " select distinct ?parent where { <" + c + "> " \
                + configuration["parent-predicate"] + " ?parent . " \
                + "FILTER(REGEX(STR(?parent), \"" + configuration["ontology-base-uri"] + "\", \"i\")) . }"

            response = self._server_manager.query_server(query)

            for c_p in response["results"]["bindings"]:
                c_p_uri = c_p["parent"]["value"]

                if c_p_uri in class_to_index:
                    c_p_index = class_to_index[c_p_uri]

                    if c_p_index not in class_parents[i]:
                        bisect.insort_left(class_parents[i], c_p_index)

                    if i not in class_children[c_p_index]:
                        bisect.insort_left(class_children[c_p_index], i)

        print("\rQuerying ontology classes subsumptions 100 %\t\t")

        ontology = Ontology(class_to_index, index_to_class, class_parents, class_children)
        return ontology, classes_per_object
