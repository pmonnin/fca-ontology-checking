import argparse

from core.factory.OntologyFactory import OntologyFactory
from core.io.ConfigurationLoader import ConfigurationLoader
from core.io.LatticeManager import LatticeManager
from core.io.ServerManager import ServerManager
from core.io.StatisticsSaver import StatisticsSaver
from core.statistics.LatticeStatistics import LatticeStatistics

__author__ = "Pierre Monnin"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configuration", help="JSON file containing the necessary configuration parameters")
    parser.add_argument("lattice", help="SOFIA lattice to annotate")
    parser.add_argument("output", help="File where the annotated SOFIA lattice will be stored")
    parser.add_argument("statistics", help="File where the statistics of the annotation will be stored")
    args = parser.parse_args()

    try:
        print("Lattice annotator")
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
                                                                  "ontology-base-uri",
                                                                  "reduce-lattice"
                                                              ])
        print("Reading lattice from file")
        lattice = LatticeManager.load_2d_sofia_lattice(args.lattice)
        server_manager = ServerManager(conf)
        print("Querying associated ontology")
        ontology_factory = OntologyFactory(server_manager)
        ontology, classes_per_object = ontology_factory.build_ontology_from_objects(lattice.get_objects(), conf)
        print("Annotating lattice")
        lattice.annotate(classes_per_object, ontology)
        if conf["reduce-lattice"]:
            lattice.reduce_to_annotated_concepts()
        print("Computing statistics")
        statistics = LatticeStatistics.compute_statistics_annotated_lattice(lattice)
        print("Saving annotated lattice")
        LatticeManager.save_annotated_lattice(args.output, lattice)
        print("Saving statistics")
        StatisticsSaver.save_statistics(statistics, args.statistics)

    except KeyError as e:
        print("Error: " + str(e))


if __name__ == '__main__':
    main()
