from queue import Queue

__author__ = "Pierre Monnin"


class LatticeStatistics:
    def __init__(self):
        pass

    @staticmethod
    def compute_statistics_2d_lattice(lattice):
        # Concepts count
        statistics = {'concepts-count': len(lattice.get_concepts()), 'arcs-count': lattice.get_arcs_count(), 'depth': 0}

        # Depth
        q = Queue()
        q.put(lattice.get_top_index())
        depth = []
        for i in range(0, statistics['concepts-count']):
            depth.append(-1)
        depth[lattice.get_top_index()] = 0

        while not q.empty():
            concept_index = q.get()

            for child_index in lattice.get_children(concept_index):
                if depth[child_index] < depth[concept_index] + 1:
                    depth[child_index] = depth[concept_index] + 1
                    q.put(child_index)

                if depth[child_index] > statistics['depth']:
                    statistics['depth'] = depth[child_index]

        return statistics

    @staticmethod
    def compute_statistics_annotated_lattice(lattice):
        statistics = LatticeStatistics.compute_statistics_2d_lattice(lattice)

        statistics["empty-annotation"] = lattice.get_empty_annotations_count()

        return statistics
