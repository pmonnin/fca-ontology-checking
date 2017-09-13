import argparse

from core.factory.OntologyFactory import OntologyFactory
from core.io.AxiomsSaver import AxiomsSaver
from core.io.ConfigurationLoader import ConfigurationLoader
from core.io.LatticeManager import LatticeManager
from core.io.ServerManager import ServerManager
from core.io.StatisticsSaver import StatisticsSaver
from core.statistics.AxiomsStatistics import AxiomsStatistics

__author__ = "Pierre Monnin"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tricontext", help="File containing the tricontext")
    parser.add_argument("projlattice",
                        help="File containing the projection of the trilattice (2D Sofia lattice) on the ontology "
                             "classes dimension")
    parser.add_argument("configuration", help="JSON file containing the necessary configuration parameters")
    parser.add_argument("axioms", help="File where the generated axioms will be stored")
    parser.add_argument("statistics", help="File where the statistics about axioms will be stored")
    args = parser.parse_args()

    try:
        print("Axioms extractor from trilattice")
        conf = ConfigurationLoader.load_n_check_configuration(args.configuration,
                                                              [
                                                                  "server-address",
                                                                  "url-json-conf-attribute",
                                                                  "url-json-conf-value",
                                                                  "url-default-graph-attribute",
                                                                  "url-default-graph-value",
                                                                  "url-query-attribute",
                                                                  "timeout",
                                                                  "type-predicate",
                                                                  "parent-predicate",
                                                                  "query-prefix",
                                                                  "ontology-base-uri"
                                                              ])

        print("Extracting objects from tricontext")
        objects = {}
        with open(args.tricontext, 'r') as tricontext:
            for i, current_line in enumerate(tricontext):
                if current_line[len(current_line) - 1] == '\n':
                    current_line = current_line[:len(current_line) - 1]

                context_entry = current_line.split(' ')
                objects[context_entry[0]] = True
        objects = list(objects.keys())
        print("Objects count: " + str(len(objects)))
        print("Reading lattice")
        lattice = LatticeManager.load_2d_sofia_lattice(args.projlattice)
        print("Querying associated ontology")
        server_manager = ServerManager(conf)
        ontology_factory = OntologyFactory(server_manager)
        ontology, classes_per_objects = ontology_factory.build_ontology_from_objects(objects, conf)
        print("Computing ontology associated to the annotated lattice")
        ontology_lattice = lattice.get_ontology_from_projection_lattice_intents(ontology)
        print("Comparing the two ontologies")
        axioms = ontology_lattice.compare_with(ontology)
        print("Computing axioms statistics")
        statistics = AxiomsStatistics.compute_statistics(axioms, ontology_lattice, ontology, classes_per_objects)
        print("Saving axioms")
        AxiomsSaver.save_axioms(axioms, args.axioms)
        print("Saving statistics")
        StatisticsSaver.save_statistics(statistics, args.statistics)

    except KeyError as e:
        print("Error: " + str(e))


if __name__ == '__main__':
    main()
