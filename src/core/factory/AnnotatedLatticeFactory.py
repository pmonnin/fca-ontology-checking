from core.fca.AnnotatedLattice import AnnotatedLattice

__author__ = "Pierre Monnin"


class AnnotatedLatticeFactory:
    def __init__(self):
        pass

    @staticmethod
    def annotate_lattice_v1(lattice, classes_per_object, ontology):
        annotated_lattice = AnnotatedLattice(lattice)

        annotated_lattice.annotate(classes_per_object, ontology)
        annotated_lattice.reduce_annotation()

        return annotated_lattice

    @staticmethod
    def annotate_lattice_v2(lattice, classes_per_object, ontology):
        annotated_lattice = AnnotatedLattice(lattice)

        annotated_lattice.annotate(classes_per_object, ontology)
        annotated_lattice.reduce_annotation()
        annotated_lattice.reduce_to_closed_annotated_concepts()

        return annotated_lattice
