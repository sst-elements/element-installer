#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import subprocess
import urllib.request

from config import ELEMENT_LIST_URL, ELEMENT_README_URL

CWD = os.getcwd()

reg_elem_re = re.compile(r"(((?<=^\d\.\s)|(?<=^\d{2}\.\s))\w*(?=.*?(?=VALID$)))", re.MULTILINE)


def _list_all_elements():
    """Grab official list of trusted elements

    The list document is a simple file with elements delimited by '\n'

    :return {List[str]}: list of elements
    """
    with urllib.request.urlopen(urllib.request.Request(ELEMENT_LIST_URL)) as elements_list:
        return elements_list.read().decode("utf-8").split()


def is_registered(element):

    reg_elements = list_registered_elements()
    if element in reg_elements:
        return True
    return False


def pprint_all_elements():
    """[summary]

    [description]
    """
    all_elements = _list_all_elements()
    print("SST Elements".ljust(25), "Registered")
    print("-" * 41)
    for element in all_elements:
        if is_registered(element):
            # print check mark (✓)
            print(element.ljust(28), "\033[32m✓\033[0m")
        else:
            print(element)


def uninstall(element):
    """Remove and uninstall element from system

    The path of the element is first located before a subprocess instance is created to avoid shell
    injection

    :param {str} element: name of element
    """
    if os.path.exists(element):
        shutil.rmtree(element)
        subprocess.call(
            f"sst-register -u {element}", shell=True
        )
        return 1
    else:
        print(f"{element} not found")


def __clone(element, user, force):
    """Clone repository of element if it is deemed official and trusted

    If element is found on `__list_all_elements()`, it will be cloned from its repository with the
    URL provided

    :param {str} element: name of element
    :param {str} user: base URL of repositories
    :param {bool} force: flag to force install. If true and element is already installed, the
                         element is re-cloned
    """
    if os.path.exists(element):
        if not force:
            print(element, "already installed")
            return
        else:
            uninstall(element)

    all_elements = _list_all_elements()
    if element in all_elements:
        subprocess.call(
            f"git clone https://github.com/{user}/{element}", shell=True, stdout=subprocess.DEVNULL
        )
    else:
        print(f"{element} not found")
        exit(1)


def __get_dependencies(element):
    """Parse dependencies of element into list

    :param {str} element: name of element

    :return {List[str]}: dependencies
    """
    print(f"Gathering dependencies for {element}...")
    with open(element + "/dependencies.txt") as req_file:
        return req_file.read().split()


def __add_dependencies(old, new):
    """Add new elements to list of dependencies

    If the new list of dependencies include elements already in the original list of dependencies,
    the index of the element is shifted to properly update the dependency graph

    :param {List{str}} old: original list of dependencies
    :param {List{str}} new: new list of elements to be added as dependencies

    :return {List{str}}: updated list of dependencies
    """
    for elem in new:
        if elem in old:
            old.remove(elem)
        old.append(elem)

    return old


def __get_var_path(elem, dep):
    """Generate Makefile variable definitions for elements with dependencies

    :param {str} elem: name of element
    :param {List{str}} dep: list of dependencies for the element

    :return {Tuple[str, str]}: name of element along with the generated Makefile variable
                               definitions
    """
    return elem, " ".join(f"{i}={CWD}/{i}" for i in dep)


def install(element, url, force=False):
    """Install element as well as its dependencies

    The element's repository is first cloned and its dependencies are determined. The dependency
    elements are then cloned as well until no more dependencies are required. All the elements are
    finally installed with their respective Makefiles in the reversed order of when they were added.

    :param {str} element: name of element
    :param {str} url: URL of element repository
    :param {bool} force: flag to force install (default: {False})
                         If true and element is already installed, the element is re-cloned
    """
    install_vars = []
    dependencies = []

    # clone the targeted element repository
    __clone(element, url, force)
    # add its dependencies as well as its Makefile variable definitions
    dependencies.extend(__get_dependencies(element))
    install_vars.append(__get_var_path(element, dependencies))

    # if the element depends on any other elements
    if dependencies:
        print(f"Found dependencies: {', '.join(dependencies)}")

        # loop through its dependencies to generate a dependency graph
        for dep in dependencies:
            __clone(dep, url, force)
            # update the list of elements to be installed along with their corresponding Makefile
            # variable definitions
            new_dependencies = __get_dependencies(dep)
            dependencies = __add_dependencies(dependencies, new_dependencies)
            install_vars.append(__get_var_path(dep, new_dependencies))
            if new_dependencies:
                print(
                    f"Found dependencies: {', '.join(new_dependencies)} (from {dep})"
                )

        # reverse the dependency graph represented in a flat array so that the parent elements are
        # installed before their children
        install_vars = install_vars[::-1]
        print("Installing dependencies...")

    # if the element does not depend on any other elements
    else:
        print("No dependencies found")

    for element, path in install_vars:
        print(f"Installing {element}...")
        subprocess.call(
            f"cd {element} && make all {path} && sst-register {element} {element}_LIBDIR={CWD} && cd -",
            shell=True, stdout=subprocess.DEVNULL
        )

    print(f"Installed {', '.join(i[0] for i in install_vars)}")
    return 0


def list_registered_elements():
    """List elements installed in system

    This function is a wrapper for the list option provided by SST

    :return {List[str]}:
    """
    elements = subprocess.check_output("$(which sst-register) -l", shell=True).decode("utf-8")
    matches = reg_elem_re.finditer(elements)
    return [match.group() for match in matches]


def get_info(element, user="sabbirahm3d"):
    """[summary]

    [description]

    Arguments:
        element {[type]} -- [description]
    """
    README_FILE_PATS = ("/README", "/README.md")
    reg_elements = list_registered_elements()
    if element in reg_elements:

        for file_name in README_FILE_PATS:
            if os.path.exists(element + file_name):
                with open(element + file_name) as readme_file:
                    return readme_file.read()

        return "No information found on " + element

    else:

        all_elements = _list_all_elements()
        if element in all_elements:
            for file_name in README_FILE_PATS:
                try:
                    return urllib.request.urlopen(
                        urllib.request.Request(
                            ELEMENT_README_URL.format(user=user, elem=element) + file_name)
                    ).read().decode("utf-8")
                except urllib.error.HTTPError:
                    continue

        return "No information found on " + element
