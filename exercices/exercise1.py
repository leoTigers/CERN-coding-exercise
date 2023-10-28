"""
The instructions don't specify the constraints of objects in the list.
Objects should at least implement the __eq__ method otherwise we can't
distinguish duplicated objects.
If all objects implement __hash__ and __eq__ methods, we can use a dict
to get the duplicated objects.
The two methods will be implemented in this file.
"""

from collections import Counter


def get_duplicated_objects_hashable(object_list: list) -> list:
    """Returns a list with the duplicated objects in the given list."""

    # dictionaries preserve insertion order
    occurrences = Counter(object_list)
    return [element for element, count in occurrences.items() if count > 1]


def get_duplicated_objects_non_hashable(object_list: list) -> list:
    """Returns a list with the duplicated objects in the given list."""

    elements_seen = []
    duplicated_elements = []
    for element in object_list:
        if element in elements_seen and element not in duplicated_elements:
            duplicated_elements.append(element)
        elements_seen.append(element)

    return duplicated_elements
