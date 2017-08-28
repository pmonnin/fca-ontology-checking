__author__ = "Pierre Monnin"


class ContextFactory:
    def __init__(self, server_manager):
        self._server_manager = server_manager

    def build_context(self, configuration_parameters):
        query = configuration_parameters["objects-selection-prefix"] + " select distinct ?object where { " \
                + configuration_parameters["objects-selection-where-clause"] + " }"

        response = self._server_manager.query_server(query)
        context = {}

        for object_json in response["results"]["bindings"]:
            object_uri = object_json["object"]["value"]

            query_attributes = configuration_parameters["attributes-selection-prefix"] \
                + " select distinct ?attribute where { " \
                + configuration_parameters["attributes-selection-where-clause"] \
                + " VALUES ?object {<" + object_uri + ">} }"

            response_attribute = self._server_manager.query_server(query_attributes)

            attributes = []
            for attribute_json in response_attribute["results"]["bindings"]:
                attributes.append(attribute_json["attribute"]["value"])

            context[object_uri] = attributes

        return context
