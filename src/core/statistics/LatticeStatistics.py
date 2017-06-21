from queue import Queue

__author__ = "Pierre Monnin"


class LatticeStatistics:
    def __init__(self):
        pass

    @staticmethod
    def compute_statistics(lattice):
        # Concepts count
        statistics = {'concepts-count': len(lattice._concepts), 'arcs-count': 0, 'depth': 0}

        # Arcs count
        for parents in lattice._parents:
            statistics['arcs-count'] += len(parents)

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
