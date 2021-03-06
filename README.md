# fca-ontology-checking

Using FCA for checking the subsumption axioms between classes of an ontology.

## Other software used

To build 2D lattices, [SOFIA](https://github.com/AlekseyBuzmakov/FCAPS) is used.

To build tri-lattices, [Data-Peeler](http://homepages.dcc.ufmg.br/~lcerf/fr/prototypes.html) is used (a docker 
containerization is available [here](https://github.com/pmonnin/datapeeler-docker)).

## Programs available

### Context creation

This program builds a context from a set of queries.
This context can either be a SOFIA context (2 dimensional) of a context for DataPeeler (tri-context). 
Statistics are computed on this context. 

[Detailed documentation](documentation/contextCreation.md)

### Lattice annotator

This programs annotates a lattice generated by SOFIA with ontology classes. Statistics are computed 
on the annotation process.

[Detailed documentation](documentation/latticeAnnotator.md)

### Tri-lattice projector

This program projects the tri-concepts on one of the 3 dimensions by building a SOFIA context corresponding 
to their projection (tri-concepts as objects and elements of the projection dimension as attributes).

[Detailed documentation](documentation/trilatticeProjector.md)

### Axioms extractor from an annotated lattice

This program extracts axioms between ontology classes from an annotated lattice. These axioms are then compared 
with the axioms existing in the ontology. Statistics are computed on the generated ontology and the comparison with 
the existing ontology.

[Detailed documentation](documentation/axiomsExtractorAnnLattice.md)

### Axioms extractor from a lattice

This program extracts axioms between ontology classes from a lattice. These axioms are then compared 
with the axioms existing in the ontology. Statistics are computed on the generated ontology and the comparison with 
the existing ontology.

[Detailed documentation](documentation/axiomsExtractorLattice.md)

### Axioms extractor from a tri-lattice

This program extracts axioms between ontology classes from a tri-lattice and its projection. These axioms are then 
compared with the axioms existing in the ontology. Statistics are computed on the generated ontology and the comparison 
with the existing ontology.

[Detailed documentation](documentation/axiomsExtractorTrilattice.md)

### SOFIA lattice statistics

This programs computes statistics on a SOFIA-generated lattice.

[Detailed documentation](documentation/sofiaLatticeStatistics.md)

### Tri-lattice statistics

This programs computes statistics on a DataPeeler-generated tri-lattice.

[Detailed documentation](documentation/trilatticeStatistics.md)

## Dependencies

* Python 3.6.1

## Publications

[1] Monnin, P., Lezoche, M., Napoli, A., & Coulet, A. (2017, June). 
Using Formal Concept Analysis for Checking the Structure of an Ontology in LOD: The Example of DBpedia. 
In 23rd International Symposium on Methodologies for Intelligent Systems, ISMIS 2017.

```bibtex
@inproceedings{monnin2017using,
  author    = {Pierre Monnin and
               Mario Lezoche and
               Amedeo Napoli and
               Adrien Coulet},
  title     = {Using {F}ormal {C}oncept {A}nalysis for Checking the Structure of an Ontology
               in {LOD:} The Example of {DB}pedia},
  booktitle = {Foundations of Intelligent Systems - 23rd International Symposium,
               {ISMIS} 2017, Warsaw, Poland, June 26-29, 2017, Proceedings},
  pages     = {674--683},
  year      = {2017},
  url       = {https://doi.org/10.1007/978-3-319-60438-1_66},
  doi       = {10.1007/978-3-319-60438-1_66}
}
```

## History

As this work is still in progress, git tags are used to identify special versions of this work.

* ``BDA-2017`` tag / release identifies the Python scripts used for the article submitted to BDA 2017
* ``DAMJ-2017`` tag / release identifies the Python scripts used for the article submitted to DAMJ (CLA 2016 
special issue)

## Contributors

[Pierre Monnin](https://pmonnin.github.io/)
