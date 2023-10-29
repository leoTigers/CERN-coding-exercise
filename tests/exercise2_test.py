"""
"""
import pytest

from exercices.exercise2 import (DependencyTree,
                                 CircularDependencyException,
                                 SelfDependencyException,
                                 NonExistingDependencyPackage)


class TestDependencyTree(object):
    def test_file_not_exists(self):
        with pytest.raises(FileNotFoundError) as exc_info:
            DependencyTree.from_json('fake')
        assert (str(exc_info.value) ==
                "[Errno 2] No such file or directory: 'fake'")

    def test_empty_dependencies(self):
        tree = DependencyTree({})
        assert str(tree) == ''

    def test_from_example_json(self):
        tree = DependencyTree.from_json('../data/test1.json')

        assert str(tree) == '''- pkg1
  - pkg2
    - pkg3
  - pkg3
- pkg2
  - pkg3
- pkg3'''

    def test_circular_dependency(self):
        with pytest.raises(CircularDependencyException) as exc_info:
            DependencyTree.from_json('../data/circular.json')
        assert str(exc_info.value) == '"pkg1" and "pkg3" depend on each other'

    def test_self_dependency(self):
        with pytest.raises(SelfDependencyException) as exc_info:
            DependencyTree.from_json('../data/self.json')
        assert str(exc_info.value) == '"pkg1" depend on itself'

    def test_depends_on_non_existing_package(self):
        with pytest.raises(NonExistingDependencyPackage) as exc_info:
            DependencyTree.from_json('../data/non_existing_dep.json')
        assert (str(exc_info.value) ==
                '"pkg1" depends on non existing child "pkg2"')
