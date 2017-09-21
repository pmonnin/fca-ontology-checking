__author__ = "Pierre Monnin"


class AxiomsStatistics:
    @staticmethod
    def compute_statistics(axioms, lattice_ontology, ontology, classes_per_objects):
        statistics = {'ontology-statistics': ontology.get_statistics(False),
                      'lattice-ontology-statistics': lattice_ontology.get_statistics(False)}

        confirmed = 0
        inferable = 0
        new = 0

        for a in axioms:
            if a[2] == "confirmed":
                confirmed += 1
            elif a[2] == "inferable":
                inferable += 1
            else:  # new
                new += 1

        statistics["axioms-count"] = {"confirmed": confirmed, "inferable": inferable, "new": new}

        common_classes = set(classes_per_objects[0])
        for i in range(1, len(classes_per_objects)):
            common_classes = common_classes & set(classes_per_objects[i])
        statistics["common-classes"] = len(common_classes)

        lattice_ontology_axioms = lattice_ontology.compute_all_axioms()
        ontology_axioms = ontology.compute_all_axioms()
        statistics["common-axioms"] = 0
        statistics["lattice-axioms"] = 0
        statistics["ontology-axioms"] = 0

        for i in range(0, len(lattice_ontology_axioms)):
            if i not in common_classes:  # Axioms cannot be expected to be found for common_classes as they're at top
                statistics["ontology-axioms"] += len(ontology_axioms[i])
                statistics["lattice-axioms"] += len(lattice_ontology_axioms[i])
                for j in lattice_ontology_axioms[i]:
                    if j in ontology_axioms[i]:
                        statistics["common-axioms"] += 1

        return statistics
