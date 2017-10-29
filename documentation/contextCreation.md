# Detailed documentation of the Context Creation program

## Purpose

This program builds a context from a set of queries.
This context can either be a SOFIA context (2 dimensional) of a context for DataPeeler (tri-context). 
Statistics are computed on this context. 

## Execution

This program can be executed with:

```bash
python contextCreation.py configuration output_context output_statistics [-t | --type]
```

with:

* _configuration_: JSON file containing the necessary configuration parameters
* _context.json_: file where the generated SOFIA/DataPeeler context will be stored
* _statistics.json_: JSON file where the statistics of the context will be stored
* _-t | --type_: type of the context to build:
    * _2D-SubjectsPredicates_: SOFIA (2D) context with subjects as objects and predicates as attributes (to be used with
    concept annotation)
    * _2D-SubjectsPredicatesClasses_: SOFIA (2D) context with subjects as objects and predicates and ontology classes 
    as attributes
    * _3D-SubjectsPredicatesClasses_: DataPeeler (3D) context with subjects as objects, predicates as attributes and 
    ontology classes as conditions


## Configuration

A JSON file is used to configure this program:

```json
{
  "server-address": "http://127.0.0.1/sparql",
  "url-json-conf-attribute": "format",
  "url-json-conf-value": "application/sparql-results+json",
  "url-default-graph-attribute": "default-graph-uri",
  "url-default-graph-value": "http://dbpedia.org",
  "timeout": 20000,
  "url-query-attribute": "query",
  "objects-selection-prefix": "",
  "objects-selection-where-clause": "",
  "attributes-selection-prefix": "",
  "attributes-selection-where-clause": "",
  "ontology-type-predicate": "rdf:type",
  "ontology-parent-predicate": "rdfs:subClassOf",
  "ontology-query-prefix": "",
  "ontology-base-uri": "http://dbpedia.org/ontology/"
}
```

with:

* _server-address_: address of the SPARQL endpoint to query
* _url-json-conf-attribute_: URL attribute to use to get JSON results
* _url-json-conf-value_: value of the _url-json-conf-attribute_ to get JSON results
* _url-default-graph-attribute_: URL attribute to use to define the default graph
* _url-default-graph-value_: value of _url-default-graph-attribute_ to define the default graph
* _url-query-attribute_: URL attribute to use to define the query
* _timeout_: timeout value for HTTP requests
* _objects-selection-prefix_: prefixes used in the query to select objects -- see next paragraphs
* _objects-selection-where-clause_: where clause used in the query to select objects -- see next paragraphs
* _attributes-selection-prefix_: prefixes used in the query to select attributes -- see next paragraphs
* _attributes-selection-where-clause_: where clause used in the query to select attributes -- see next paragraphs

Only available for _2D-SubjectsPredicatesClasses_ or _3D-SubjectsPredicatesClasses_:

* _ontology-type-predicate_: predicate used to type subjects with an ontology class -- see next paragraphs
* _ontology-parent-predicate_: predicate used to express subsumption axioms in the considered ontology -- see next 
paragraphs
* _ontology-query-prefix_: prefixes used in the queries associated with the ontology classes selection -- see next 
paragraphs
* _ontology-base-uri_: base URI for ontology classes -- see next paragraphs

## SPARQL queries

Below are the SPARQL queries used in the Python scripts. The use of configuration parameters is highlighted 
with ``("parameter_used")``.

### Selection of objects

```sparql
("objects-selection-prefix")

select distinct ?object where {
    ("objects-selection-where-clause")
}
```

### Selection of attributes

For each object, identified by its ``object_uri``:

```sparql
("attributes-selection-prefix")

select distinct ?attribute where {
    ("attributes-selection-where-clause")
    VALUES ?object { <object_uri> }
}
```

### Selection of ontology classes

For each object, identified by its ``object_uri``:

```sparql
("ontology-query-prefix")

select distinct ?class where {
    <object_uri> ("ontology-type-predicate")/("ontology-parent-predicate")* ?class .
    FILTER(REGEX(STR(?class), "(ontology-base-uri)", "i")) .
}
```
