"""
I will assume json file has the format required by the exercise.

Instructions don't mention circular dependencies,
but I'm assuming that's a possibility.

Instruction don't mention dependency order,
so I'm assuming it will be arbitrary.

Instruction don't mention the possibility of a dependency appearing
multiples times for a package, if that's the case the duplicated
dependencies will be ignored.
"""

import json
import sys


class CircularDependencyException(Exception):
    """
    Exception for packages depending on parent packages
    """
    def __init__(self, package1: str, package2: str):
        if package1 == package2:
            raise SelfDependencyException(package1)
        else:
            super().__init__(f'"{package1}" and "{package2}" '
                             f'depend on each other')


class SelfDependencyException(Exception):
    """
    Exception for packages depending on themselves
    """
    def __init__(self, package: str):
        super().__init__(f'"{package}" depend on itself')


class NonExistingDependencyPackage(Exception):
    """
    Exception for packages depending on non referenced packages
    """
    def __init__(self, parent: str, child: str):
        super().__init__(f'"{parent}" depends on non existing child "{child}"')


class DependencyTree(object):
    """
    Class representing the dependency tree
    Can be constructed from a dictionnary
    or from a json file with the from_json() method
    """
    def __init__(self, dependencies: dict[str, list]):
        self.dependencies = dependencies
        self.tree = {}
        for key in dependencies.keys():
            self.tree[key] = self.expand(key)

    def expand(self, package_name: str,
               dependencies_seen: list[str] = None) -> dict[str, dict]:
        """
        Expand the tree dependencies with sub-dependencies recursively
        :param package_name: the package name
        :param dependencies_seen: list of packages seen so far to detect
        circular dependencies
        :return: Returns all sub-dependencies for a package
        """

        if dependencies_seen is None:
            dependencies_seen = []

        sub_tree = {}
        # check if the dependency exists in our dependency dictionary
        if package_name not in self.dependencies:
            raise NonExistingDependencyPackage(dependencies_seen[-1],
                                               package_name)

        for dep in self.dependencies[package_name]:
            # check for circular dependencies
            if dep in dependencies_seen:
                raise CircularDependencyException(dep, package_name)
            # ignore duplicates dependencies
            if dep in sub_tree:
                continue

            sub_tree[dep] = self.expand(dep,
                                        dependencies_seen + [package_name])
        return sub_tree

    @classmethod
    def from_json(cls, jsonfile: str) -> "DependencyTree":
        """
        Construct a DependencyTree from a json file
        :param jsonfile: path to the json file
        :return: A DependencyTree corresponding to the json data
        """
        with open(jsonfile, 'r') as file:
            data = json.load(file)

        return cls(data)

    def dependency_to_string(self, dependencies: dict, indent: int = 0) -> str:
        """
        Helper method to recursively transform the dependency tree in a string
        :param dependencies: the current dependency to convert
        :param indent: indentation corresponding to the depth of
        the subpackage
        :return: the string corresponding to the subpackage
        """
        lines = []
        for key, value in dependencies.items():
            lines.append(f'{indent * "  "}- {key}')
            string = self.dependency_to_string(dependencies[key], indent + 1)
            if string:  # ignore empty strings from empty dependencies
                lines.append(string)
        return '\n'.join(lines)

    def __str__(self) -> str:
        return self.dependency_to_string(self.tree)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide a json file')
        exit(1)

    file = sys.argv[1]
    tree = DependencyTree.from_json(file)
    print(tree)
