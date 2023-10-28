from exercices.exercise1 import (get_duplicated_objects_hashable,
                                 get_duplicated_objects_non_hashable)


class TestGetDuplicatedObjectsHashable:
    def test_empty_list(self):
        assert get_duplicated_objects_hashable([]) == []

    def test_no_duplicates(self):
        assert get_duplicated_objects_hashable([1, 2, 3]) == []

    def test_duplicates(self):
        assert get_duplicated_objects_hashable([1, 1, 2, 3, 3]) == [1, 3]

    def test_duplicates_out_of_order(self):
        assert get_duplicated_objects_hashable([3, 2, 3, 1, 1]) == [3, 1]

    def test_hashable_class(self):
        class HashableClass:
            def __init__(self, value):
                self.value = value

            def __hash__(self):
                return hash(self.value)

            def __eq__(self, other):
                return self.value == other.value

        assert (get_duplicated_objects_hashable(
            [HashableClass(1), HashableClass(1), HashableClass(2)]) ==
                [HashableClass(1)])


class TestGetDuplicatedObjectsNonHashable:
    def test_empty_list(self):
        assert get_duplicated_objects_non_hashable([]) == []

    def test_no_duplicates(self):
        assert get_duplicated_objects_non_hashable([1, 2, 3]) == []

    def test_duplicates(self):
        assert get_duplicated_objects_non_hashable([1, 1, 2, 3, 3]) == [1, 3]

    def test_duplicates_out_of_order(self):
        assert get_duplicated_objects_non_hashable([3, 2, 3, 1, 1]) == [3, 1]

    def test_hashable_class(self):
        class HashableClass:
            def __init__(self, value):
                self.value = value

            def __hash__(self):
                return hash(self.value)

            def __eq__(self, other):
                return self.value == other.value

        assert (get_duplicated_objects_non_hashable(
            [HashableClass(1), HashableClass(1), HashableClass(2)]) ==
                [HashableClass(1)])
