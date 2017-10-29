# Detailed documentation of the Axioms Extractor from an Annotated Lattice program

## Purpose

This program extracts axioms between ontology classes from a tri-lattice and its projection. These axioms are then 
compared with the axioms existing in the ontology. Statistics are computed on the generated ontology and the comparison 
with the existing ontology.

## Execution

This program can be executed with:

```bash
python axiomsExtractorTriLattice.py tricontext projlattice configuration axioms statistics
```

with:

* _tricontext_: File containing the tricontext
* _projlattice_: File containing the projection of the trilattice (2D Sofia lattice) on the ontology classes dimension
* _configuration_: JSON file containing the necessary configuration parameters
* _axioms_: File where the generated axioms will be stored
* _statistics_: File where the statistics about axioms will be stored

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
  "type-predicate": "rdf:type",
  "parent-predicate": "rdfs:subClassOf",
  "query-prefix": "",
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
* _type-predicate_: predicate used to express class instantiation
* _parent-predicate_: predicate used to express subsumption axioms in the considered ontology
* _query-prefix_*: prefixes to be used when querying the existing ontology
* _ontology-base-uri_: base URI of the ontology

## SPARQL queries

Below are the SPARQL queries used in the Python scripts. The use of configuration parameters is highlighted 
with ``("parameter_used")``.

### Selection of classes

For each object ``o`` of the annotated lattice:

```sparql
("query-prefix")

select distinct ?class where {
    <o> ("type-predicate")/("parent-predicate")* ?class .
    FILTER(REGEX(STR(?class), "(ontology-base-uri)", "i")) .
}
```

### Relationships between classes

For each class of the ontology identified with its ``class_uri``:

```sparql
("query-prefix")

select distinct ?parent where {
    <class_uri> ("parent-predicate") ?parent . 
    FILTER(REGEX(STR(?parent), "(ontology-base-uri)", "i")) .
}
```
