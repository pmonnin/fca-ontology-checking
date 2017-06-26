import sys

from core.factory.AnnotatedLatticeFactory import AnnotatedLatticeFactory
from core.factory.OntologyFromObjectsFactory import OntologyFromObjectsFactory
from core.io.AxiomsSaver import AxiomsSaver
from core.io.ConfigurationLoader import ConfigurationLoader
from core.io.ServerManager import ServerManager
from core.io.SofiaLatticeLoader import SofiaLatticeLoader
from core.io.StatisticsSaver import StatisticsSaver
from core.statistics.AnnotationStatistics import AnnotationStatistics

__author__ = "Pierre Monnin"


def main():
    if len(sys.argv) != 5:
        print_usage()

    else:
        try:
            print("Lattice annotator")
            conf = ConfigurationLoader.load_n_check_configuration(sys.argv[1],
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
            lattice = SofiaLatticeLoader.load_lattice(sys.argv[2])
            server_manager = ServerManager(conf)
            print("Querying associated ontology")
            ontology, classes_per_object = OntologyFromObjectsFactory.build_factory_from_objects(lattice,
                                                                                                 server_manager, conf)
            print("Annotating lattice")
            annotated_lattice = None
            if conf["reduce-lattice"]:
                annotated_lattice = AnnotatedLatticeFactory.annotate_lattice_v2(lattice, classes_per_object, ontology)
            else:
                annotated_lattice = AnnotatedLatticeFactory.annotate_lattice_v1(lattice, classes_per_object, ontology)
            print("Extracting subsumption axioms from annotated lattice")
            lattice_ontology = annotated_lattice.get_ontology_schema_from_lattice()
            print("Comparing axioms with associated ontology")
            axioms = lattice_ontology.compare_with(ontology)
            AxiomsSaver.save_axioms(axioms, ontology, sys.argv[3])
            print("Computing annotation statistics")
            statistics = AnnotationStatistics.compute_statistics(ontology, lattice_ontology, annotated_lattice, axioms,
                                                                 classes_per_object)
            StatisticsSaver.save_statistics(statistics, sys.argv[4])

        except KeyError as e:
            print("Error: " + str(e))


def print_usage():
    print("Usage: latticeAnnotator.py config.json lattice.json output.csv statistics.json")
    print("\tconfig.json\tJSON file containing the necessary configuration parameters")
    print("\tlattice.json\t")
    print("\toutput.csv\tName of the file where the resulting subsumptions will be stored")
    print("\tstatistics.json\tName of the file where the statistics of the annotation will be stored")

if __name__ == '__main__':
    main()
