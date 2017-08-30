__author__ = "Pierre Monnin"


class ContextFactory:
    def __init__(self, server_manager):
        self._server_manager = server_manager

    def build_context_subjects_predicates(self, configuration_parameters):
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

    def build_context_subjects_predicates_classes_2d(self, configuration_parameters):
        context = self.build_context_subjects_predicates(configuration_parameters)

        for object_uri in context.keys():
            query_classes = configuration_parameters["ontology-query-prefix"] \
                + " select distinct ?class where { <" + object_uri + "> " \
                + configuration_parameters["ontology-type-predicate"] + "/" \
                + configuration_parameters["ontology-parent-predicate"] + "* ?class . " \
                + "FILTER(REGEX(STR(?class), \"" + configuration_parameters["ontology-base-uri"] + "\", \"i\")) . }"

            response_classes = self._server_manager.query_server(query_classes)
            for ontology_class_json in response_classes["results"]["bindings"]:
                context[object_uri].append(ontology_class_json["class"]["value"])

        return context

    def build_context_subjects_predicates_classes_3d(self, configuration_parameters):
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

            query_classes = configuration_parameters["ontology-query-prefix"] \
                + " select distinct ?class where { <" + object_uri + "> " \
                + configuration_parameters["ontology-type-predicate"] + "/" \
                + configuration_parameters["ontology-parent-predicate"] + "* ?class . " \
                + "FILTER(REGEX(STR(?class), \"" + configuration_parameters["ontology-base-uri"] + "\", \"i\")) . }"

            response_classes = self._server_manager.query_server(query_classes)
            classes = []
            for ontology_class_json in response_classes["results"]["bindings"]:
                classes.append(ontology_class_json["class"]["value"])

            context[object_uri] = {}
            for attribute_json in response_attribute["results"]["bindings"]:
                context[object_uri][attribute_json["attribute"]["value"]] = list(classes)

        return context
