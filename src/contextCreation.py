import argparse

from core.factory.ContextFactory import ContextFactory
from core.io.StatisticsSaver import StatisticsSaver
from core.io.ConfigurationLoader import ConfigurationLoader
from core.io.ServerManager import ServerManager
from core.io.ContextManager import ContextManager
from core.statistics.ContextStatistics import ContextStatistics

__author__ = "Pierre Monnin"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("configuration", help="JSON file containing the necessary configuration parameters")
    parser.add_argument("output_context", help="JSON file where the generated SOFIA/DataPeeler context will be stored")
    parser.add_argument("output_statistics", help="JSON file where the statistics of the context will be stored")
    parser.add_argument("-t", "--type", help="Context type", choices=['2D-SubjectsPredicates',
                                                                      '2D-SubjectsPredicatesClasses',
                                                                      '3D-SubjectsPredicatesClasses'],
                        default="PagesPredicates")
    args = parser.parse_args()

    print("Context creation")
    try:
        if args.type == "2D-SubjectsPredicatesClasses" or args.type == "3D-SubjectsPredicatesClasses":
            conf = ConfigurationLoader.load_n_check_configuration(args.configuration,
                                                                  [
                                                                      "server-address",
                                                                      "url-json-conf-attribute",
                                                                      "url-json-conf-value",
                                                                      "url-default-graph-attribute",
                                                                      "url-default-graph-value",
                                                                      "url-query-attribute",
                                                                      "timeout",
                                                                      "objects-selection-prefix",
                                                                      "objects-selection-where-clause",
                                                                      "attributes-selection-prefix",
                                                                      "attributes-selection-where-clause",
                                                                      "ontology-type-predicate",
                                                                      "ontology-parent-predicate",
                                                                      "ontology-query-prefix",
                                                                      "ontology-base-uri"
                                                                  ])
        else:  # 2D-PagesPredicates
            conf = ConfigurationLoader.load_n_check_configuration(args.configuration,
                                                                  [
                                                                      "server-address",
                                                                      "url-json-conf-attribute",
                                                                      "url-json-conf-value",
                                                                      "url-default-graph-attribute",
                                                                      "url-default-graph-value",
                                                                      "url-query-attribute",
                                                                      "timeout",
                                                                      "objects-selection-prefix",
                                                                      "objects-selection-where-clause",
                                                                      "attributes-selection-prefix",
                                                                      "attributes-selection-where-clause"
                                                                  ])

        server_manager = ServerManager(conf)
        context_factory = ContextFactory(server_manager)

        if args.type == "2D-SubjectsPredicates":
            context = context_factory.build_context_subjects_predicates(conf)
            ContextManager.save_2d_context_for_sofia(context, args.output_context)
            statistics = ContextStatistics.compute_2d_context_statistics(context)
        elif args.type == "2D-SubjectsPredicatesClasses":
            context = context_factory.build_context_subjects_predicates_classes_2d(conf)
            ContextManager.save_2d_context_for_sofia(context, args.output_context)
            statistics = ContextStatistics.compute_2d_context_statistics(context)
        else:  # 3D-SubjectsPredicatesClasses
            context = context_factory.build_context_subjects_predicates_classes_3d(conf)
            ContextManager.save_3d_context_for_data_peeler(context, args.output_context)
            statistics = ContextStatistics.compute_3d_context_statistics(context)

        StatisticsSaver.save_statistics(statistics, args.output_statistics)

    except KeyError as e:
        print("Error: " + str(e))


if __name__ == '__main__':
    main()
