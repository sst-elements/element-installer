#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script provides the functionality required to manage SST elements in a system.

The functionalities include:
    - listing possible elements
    - listing elements registered on system
    - gathering dependency of elements
    - gathering README content of elements
    - cloning elements and its dependencies
    - installing elements and its dependencies to the system
    - uninstalling elements from the system
    - uninstalling dependent elements from the system
    - gathering version of SST Core installed in the system
"""
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request

REG_ELEM_RE = re.compile(r"(((?<=^\d\.\s)|(?<=^\d{2}\.\s))\w*(?=.*?(?=VALID$)))", re.MULTILINE)

ELEMENT_LIST_URL = os.environ.get("ELEMENT_LIST_URL", None)
ELEMENT_SRC_DIR = os.environ.get("ELEMENT_SRC_DIR", None)

if not (ELEMENT_LIST_URL and ELEMENT_SRC_DIR):
    raise KeyError("Environment variables not set up properly")

os.chdir(ELEMENT_SRC_DIR)

INSTALLED_ELEMS = ""


def get_version():
    """Get version of SST installed on system

    Returns:
    --------
    str
        version string of SST
    """
    return subprocess.check_output("$(which sst) -V || true", shell=True).decode("utf-8")


def __clone(element, force, branch, head):
    """Clone repository of element if it is deemed official and trusted

    If element is found on `_list_all_elements()`, it will be cloned from its repository with the
    URL provided

    Parameters:
    -----------
    element : str
        name of element
    force : bool
        flag to force install. If true and element is already installed, the element is re-cloned
    branch : str
        branch of repository of the element
    head : str
        commit SHA to revert to in the repository of the element

    Raises:
    -------
    urllib.error.URLError
        cloning of element's repository failed
    FileNotFoundError
        requested element does not exist

    Returns:
    --------
    bool
        if element was clone
    """
    if os.path.exists(element):
        if not force:
            print(f"{element} already installed")
            return False
        else:
            uninstall(element)

    all_elements = list_all_elements()
    all_element_names = all_elements.keys()
    if element in all_element_names:
        # git clone failed if exit code is non-zero
        if subprocess.call(
            f"git clone -q -b {branch} --single-branch {all_elements[element]['url']}",
            shell=True, stdout=subprocess.DEVNULL
        ):
            raise urllib.error.URLError(f"Cloning of repository for {element} failed")

        else:
            if head:
                subprocess.call(f"cd {element} && git reset --hard {head} && cd -", shell=True,
                                stdout=subprocess.DEVNULL)
            return True

    else:
        raise FileNotFoundError(f"{element} not found")


def get_dependencies(element):
    """Parse dependencies of element into list

    Parameters:
    -----------
    element : str
        name of element

    Raises:
    -------
    FileNotFoundError
        requested element does not exist

    Returns:
    --------
    list(str)
        dependencies of element
    """
    all_elements = list_all_elements()
    if element in all_elements.keys():
        return all_elements[element]["dep"]

    raise FileNotFoundError(f"{element} not found")


def __add_dependencies(old, new):
    """Add new elements to list of dependencies

    If the new list of dependencies include elements already in the original list of dependencies,
    the index of the element is shifted to properly update the dependency graph

    Parameters:
    -----------
    old : list(str)
        original list of dependencies
    new : list(str)
        new list of elements to be added as dependencies

    Returns:
    --------
    list(str)
        updated list of dependencies
    """
    for _element in new:
        if _element in old:
            old.remove(_element)
        old.append(_element)

    return old


def __get_var_path(dep):
    """Generate Makefile variable definitions for elements with dependencies

    Parameters:
    -----------
    dep : list(str)
        list of dependencies for the element

    Returns:
    --------
    str
        name of element along with the generated Makefile variable definitions
    """
    return " ".join(f"{i}={ELEMENT_SRC_DIR}{i}" for i in dep)


def install(element, force=False, branch="master", head=""):
    """Install element as well as its dependencies

    The element's repository is first cloned and its dependencies are determined. The dependency
    elements are then cloned as well until no more dependencies are required. All the elements are
    finally installed with their respective Makefiles in the reversed order of when they were added.

    Parameters:
    -----------
    element : str
        name of element
    force : bool (default: False)
        flag to force install. If true and element is already installed, the
        element is re-cloned
    branch : str (default: "master")
        branch of repository of the element
    head : str (default: "")
        commit SHA to revert to in the repository of the element

    Returns:
    --------
    int
        return code for the GUI wrapper. Return 0 on success, 2 on failure.
    """
    install_vars = []
    dependencies = []

    # clone the targeted element repository
    if __clone(element, force, branch, head):

        # add its dependencies as well as its Makefile variable definitions
        print(f"Gathering dependencies for {element}...")
        dependencies.extend(get_dependencies(element))
        install_vars.append((element, __get_var_path(dependencies)))

        # if the element depends on any other elements
        if dependencies:
            print(f"Found dependencies: {', '.join(dependencies)}")

            # loop through its dependencies to generate a dependency graph
            for dep in dependencies:

                if __clone(dep, force):

                    # update the list of elements to be installed along with their corresponding
                    # Makefile variable definitions
                    print(f"Gathering dependencies for {dep}...")
                    new_dependencies = get_dependencies(dep)
                    dependencies = __add_dependencies(dependencies, new_dependencies)
                    install_vars.append((dep, __get_var_path(new_dependencies)))
                    if new_dependencies:
                        print(
                            f"Found dependencies: {', '.join(new_dependencies)} (from {dep})"
                        )
                    else:
                        print(f"No dependencies found for {dep}")

            # reverse the dependency graph represented in a flat array so that the parent elements
            # are installed before their children
            install_vars = install_vars[::-1]
            print("Installing dependencies...")

        # if the element does not depend on any other elements
        else:
            print("No dependencies found")

        for element, path in install_vars:
            print(f"Installing {element}... ", end="", flush=True)
            subprocess.call(
                f"cd {element} && make all {path} && sst-register {element} {element}_LIBDIR={ELEMENT_SRC_DIR}{element} && cd -",
                shell=True, stdout=subprocess.DEVNULL
            )
            print("done")

        global INSTALLED_ELEMS
        INSTALLED_ELEMS = f"Installed {', '.join([i[0] for i in install_vars])}"
        print(INSTALLED_ELEMS)
        return 0

    return 2


def __get_dependents(element):
    """Gather elements that are dependent on the target element

    Parameters:
    -----------
    element : str
        name of element

    Returns:
    --------
    list(str)
        list of element names flagged as dependents of the target element
    """
    all_elements = list_all_elements()
    reg_elements = list_registered_elements()
    dependents = []
    if element in reg_elements:
        for _element in reg_elements:
            if element in all_elements[_element]["dep"]:
                dependents.append(_element)

    return dependents


def uninstall(element, clean=False):
    """Remove and uninstall element from system

    The path of the element is first located before a subprocess instance is created to avoid shell
    injection

    Parameters:
    -----------
    element : str
        name of element
    clean : bool (default: False)
        flag to remove element as well as its dependent elements. This option is useful in cleaning
        up deprecated elements.

    Returns:
    --------
    int
        return code for the GUI wrapper. Return 1 on success, 2 on failure.
    """
    elements = [element]
    if clean:
        elements += __get_dependents(element)

    for _element in elements:
        if os.path.exists(_element):
            shutil.rmtree(_element)
            subprocess.call(
                f"sst-register -u {_element}", shell=True, stdout=subprocess.DEVNULL
            )
            print(f"{_element} uninstalled successfully")

        else:
            print(f"{_element} not found")
            return 2

    return 1


def get_info(element):
    """Get README of element

    If the element is installed, the local README contents and its path are returned. Else, the
    README contents are grabbed from the element's repository.

    Parameters:
    -----------
    element : str
        name of element

    Raises:
    -------
    FileNotFoundError
        requested element does not exist

    Returns:
    --------
    str
        README content
    str
        path or URL to README
    """
    README_FILE_PATS = ("/README.md", "/README")
    reg_elements = list_registered_elements()
    if element in reg_elements:

        for file_name in README_FILE_PATS:
            if os.path.exists(element + file_name):
                with open(element + file_name) as readme_file:
                    return readme_file.read(), element + file_name

    else:

        all_elements = list_all_elements()
        all_element_names = all_elements.keys()
        if element in all_element_names:
            for file_name in README_FILE_PATS:
                readme_url = all_elements[element]["url"].replace("github", "raw.githubusercontent")
                try:
                    readme_file = urllib.request.urlopen(f"{readme_url}/master/{file_name}")
                except urllib.error.HTTPError:
                    continue
                else:
                    with readme_file:
                        return readme_file.read().decode("utf-8"), all_elements[element]["url"]

    # if an invalid element is requested
    raise FileNotFoundError(f"No information found on {element}")


def list_all_elements():
    """Grab official list of trusted elements

    Raises:
    -------
    FileNotFoundError
        element list file cannot be found due to a broken path
    urllib.error.HTTPError
        other HTTP errors

    Returns:
    --------
    dict(str, str)
        key-value pairs of elements mapped to their repository URLs
    """
    try:
        elements_list_file = urllib.request.urlopen(ELEMENT_LIST_URL)

    except urllib.error.HTTPError as exc:
        raise FileNotFoundError("Elements list file not found") from exc if exc.code == 404 else exc

    else:
        with elements_list_file:
            return json.loads(elements_list_file.read().decode("utf-8"))


def is_registered(element):
    """Check if element is registered in system

    Parameters
    ----------
    element : str
        name of element

    Returns:
    --------
    bool
        if element is registered
    """
    return element in list_registered_elements()


def list_registered_elements():
    """List elements installed in system

    This function is a wrapper for the list option provided by SST

    Returns:
    --------
    list(str)
        list of registered elements
    """
    elements = subprocess.check_output("$(which sst-register) -l", shell=True).decode("utf-8")
    matches = REG_ELEM_RE.finditer(elements)
    return [match.group() for match in matches]
