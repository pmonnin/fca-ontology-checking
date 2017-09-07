# Basic data
top = 1
bottom = 6
objects = ["e1", "e2", "e3", "e4"]
attributes = ["rdf:type", "pred1", "pred2", "pred3"]
concepts = [
    {'extent': [0, 1, 2, 3], 'intent': [0]},
    {'extent': [0, 1, 3], 'intent': [0, 2]},
    {'extent': [0, 1, 2], 'intent': [0, 1]},
    {'extent': [1, 3], 'intent': [0, 2, 3]},
    {'extent': [0, 1], 'intent': [0, 1, 2]},
    {'extent': [1], 'intent': [0, 1, 2, 3]},
]
concepts_parents = [
    [],
    [0],
    [0],
    [1],
    [1, 2],
    [3, 4]
]
concepts_children = [
    [1, 2],
    [3, 4],
    [4],
    [5],
    [5],
    []
]
classes_per_object = [
    [0, 1, 2],
    [0, 1, 2, 3, 4],
    [0, 1, 2],
    [0, 1, 2, 4]
]
class_to_index = {
    'k1': 0,
    'k2': 1,
    'k3': 2,
    'k4': 3,
    'k5': 4
}
index_to_class = [
    "k1",
    "k2",
    "k3",
    "k4",
    "k5"
]
class_parents = [
    [],
    [2],
    [],
    [],
    []
]
class_children = [
    [],
    [],
    [1],
    [],
    []
]
