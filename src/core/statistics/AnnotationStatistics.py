__author__ = "Pierre Monnin"


class AnnotationStatistics:
    def __init__(self):
        pass

    @staticmethod
    def compute_statistics(data_ontology, lattice_ontology, annotated_lattice, axioms, classes_per_object):
        statistics = {
                        'data-ontology-statistics': data_ontology.get_statistics(),
                        'lattice-ontology-statistics': lattice_ontology.get_statistics(),
                        'empty-annotations': annotated_lattice.get_number_of_empty_annotations()
                     }

        new = 0
        inferable = 0
        confirmed = 0
        for a in axioms:
            if a[2] == "new":
                new += 1

            elif a[2] == "inferable":
                inferable += 1

            else:
                confirmed += 1

        statistics["new-axioms"] = new
        statistics["inferable"] = inferable
        statistics["confirmed"] = confirmed

        axioms_lattice = lattice_ontology.compute_all_axioms()
        axioms_ontology = data_ontology.compute_all_axioms()

        found_axioms = 0
        total_axioms = 0
        for i in range(0, len(lattice_ontology._index_to_class)):
            for j in axioms_lattice[i]:
                if j in axioms_ontology[i]:
                    found_axioms += 1

            total_axioms += len(axioms_ontology[i])
        statistics["found-existing-axioms"] = found_axioms
        statistics["expected-existing-axioms"] = total_axioms

        common_classes = set(classes_per_object[0])
        for i in range(1, len(classes_per_object)):
            common_classes = common_classes & set(classes_per_object[i])
        statistics["common-classes"] = len(common_classes)

        if len(common_classes) != 0:
            corr_found_axioms = 0
            corr_total_axioms = 0

            for i in range(0, len(lattice_ontology._index_to_class)):
                if i not in common_classes:
                    for j in axioms_lattice[i]:
                        if j in axioms_ontology[i]:
                            corr_found_axioms += 1

                    corr_total_axioms += len(axioms_ontology[i])
            statistics["corrected-found-existing-axioms"] = corr_found_axioms
            statistics["corrected-expected-existing-axioms"] = corr_total_axioms

        return statistics
