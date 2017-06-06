import sys

from core.factory.ContextFactory import ContextFactory
from core.io.ConfigurationLoader import ConfigurationLoader
from core.io.ServerManager import ServerManager
from core.io.SofiaBinaryContextManager import SofiaBinaryContextManager

__author__ = "Pierre Monnin"


def main():
    print("Context creation")

    if len(sys.argv) != 3:
        print_usage()

    else:
        try:
            conf = ConfigurationLoader.load_n_check_configuration(sys.argv[1],
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
            context = context_factory.build_context(conf)
            SofiaBinaryContextManager.save_context(context, sys.argv[2])

        except KeyError as e:
            print("Error: " + str(e))


def print_usage():
    print("Usage: contextCreation.py conf-context-creation.json context.json")
    print("\tconf-context-creation.json\tJSON file containing the necessary configuration parameters")
    print("\tcontext.json\tName of the file where the generated SOFIA context will be stored")

if __name__ == '__main__':
    main()
