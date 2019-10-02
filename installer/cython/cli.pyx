#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import urllib.request

# single official list of all trusted elements
ELEMENT_LIST_URL = "https://raw.githubusercontent.com/sabbirahm3d/sst-elements/standalone/elements"

# official repository collection of all elements
ELEMENT_REPO_URL = "https://github.com/sabbirahm3d/"

CWD = os.getcwd()


def list_all_elements():
    """Grab official list of trusted elements

    The list document is a simple file with elements delimited by '\n'

    :return: list of elements
    """
    with urllib.request.urlopen(ELEMENT_LIST_URL) as elements_list:
        return elements_list.read().decode("utf-8").split()


cdef void uninstall(str element):
    """Remove and uninstall element from system

    The path of the element is first located before a subprocess instance is created to avoid shell
    injection

    :param element: name of element
    """

    if os.path.exists(element):
        shutil.rmtree(element)
        subprocess.call(
            f"sst-register -u {element}", shell=True
        )
    else:
        print(f"{element} not found")


cdef void __clone(str element, str url, bint force):
    """Clone repository of element if it is deemed official and trusted

    If element is found on `list_all_elements()`, it will be cloned from its repository with the
    URL provided

    :param element: name of element
    :param url: base URL of repositories
    :param force: flag to force install. If true and element is already installed, the element is re-cloned
    """
    if os.path.exists(element):
        if not force:
            print(element, "already installed")
            return
        else:
            uninstall(element)

    if element in list_all_elements():
        subprocess.call(
            f"git clone {url}{element}", shell=True, stdout=subprocess.DEVNULL
        )
    else:
        print(f"{element} not found")
        exit(1)


cdef __get_dependencies(str element):
    """Parse dependencies of element into list

    :param element: name of element

    :return: dependencies
    """
    print(f"Gathering dependencies for {element}...")
    with open(element + "/dependencies.txt") as req_file:
        return req_file.read().split()


def __add_dependencies(old, new):
    """Add new elements to list of dependencies

    If the new list of dependencies include elements already in the original list of dependencies,
    the index of the element is shifted to properly update the dependency graph

    :param old {list{str}}: original list of dependencies
    :param new {list{str}}: new list of elements to be added as dependencies

    :return {list{str}}: updated list of dependencies
    """
    for elem in new:
        if elem in old:
            old.remove(elem)
        old.append(elem)

    return old


def __get_var_path(elem, dep):
    """Generate Makefile variable definitions for elements with dependencies

    :param elem: name of element
    :param dep: list of dependencies for the element

    :return: name of element along with the generated Makefile variable definitions
    """
    return elem, " ".join(f"{i}={CWD}/{i}" for i in dep)


cdef void install(str element, str url, bint force = False):
    """Install element as well as its dependencies

    The element's repository is first cloned and its dependencies are determined. The dependency
    elements are then cloned as well until no more dependencies are required. All the elements are
    finally installed with their respective Makefiles in the reversed order of when they were added.

    :param element: name of element
    :param url: URL of element repository
    :param force: flag to force install (default: {False})
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


cdef void list_elems():
    """List elements installed in system

    This function is a wrapper for the list option provided by SST
    """
    subprocess.call("sst-register -l", shell=True)


if __name__ == "__main__":

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="SST Element Installer")
    parser.add_argument("--install", "-i", metavar="ELEMENT", type=str, default="",
                        help="Install element")
    parser.add_argument("--uninstall", "-u", metavar="ELEMENT", type=str, default="",
                        help="Uninstall element")
    parser.add_argument("--force", "-f", action="store_true", default=False)
    parser.add_argument("--list", "-l", action="store_true", default=False)
    parser.add_argument("--url", "-x", type=str, default=ELEMENT_REPO_URL)

    args: argparse.Namespace = parser.parse_args()

    # install and uninstall options are mutually exclusive
    if args.install and args.uninstall:
        parser.print_help()
        exit(1)

    elif args.install:
        install(args.install, args.url, args.force)

    elif args.uninstall:
        uninstall(args.uninstall)

    elif args.list:
        list_elems()

    else:
        parser.print_help()
