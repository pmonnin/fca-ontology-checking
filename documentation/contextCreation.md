# Detailed documentation of the Context Creation program

## Purpose

This program builds a SOFIA context from a set of queries to select objects and their associated 
attributes.

## Configuration

[A configuration example is available](../examples/conf-context-creation.json). It contains:

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
  "attributes-selection-where-clause": ""
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

## Execution

This program can be executed with:

```shell
python contextCreation.py conf-context-creation.json context.json
```

with:

* _conf-context-creation.json_: path to the configuration file -- see previous paragraphs
* _context.json_: SOFIA context built from the configuration and the executed SPARQL queries
