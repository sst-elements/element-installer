#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import urllib.request

ELEMENT_LIST_URL = "https://raw.githubusercontent.com/sabbirahm3d/sst-elements/standalone/elements"


def get_elements():
    with urllib.request.urlopen(ELEMENT_LIST_URL) as elements_list:
        return elements_list.read().decode("utf-8").split()


def uninstall(element):

    if os.path.exists(element):
        shutil.rmtree(element)
        command = "sst-register -u {}".format(element)
        subprocess.call(command, shell=True)
    else:
        print(f"{element} not found")


def clone(element, url, force=False):
    if os.path.exists(element):
        if not force:
            print(element, "already installed")
            return
        else:
            uninstall(element)
    if element in get_elements():
        command = "git clone {url}{element}".format(url=url, element=element)
        subprocess.call(command, shell=True)
    else:
        print(f"{element} not found")
        exit(1)


def get_requirements(element):

    print(f"Gathering dependencies for {element}...")
    with open(element + "/requirements.txt") as req_file:
        return req_file.read().split()


def install(element, url, force=False):

    requirements = []

    def __add_requirements(old, new):

        for elem in new:
            if elem in old:
                old.remove(elem)
            old.append(elem)

        return old

    clone(element, url, force)
    requirements.extend(get_requirements(element))
    if requirements:
        print(f"Found dependencies: {', '.join(requirements)}")
        for i in requirements:
            clone(i, url, force)
            new_requirements = get_requirements(i)
            requirements = __add_requirements(requirements, new_requirements)
            if new_requirements:
                print(
                    f"Found dependencies: {', '.join(new_requirements)} (from {i})"
                )

        requirements = requirements[::-1] + [element]
        print("Installing dependencies...")
    else:
        print("No dependencies found")

    for element in requirements:
        print(f"Installing {element}...")
        subprocess.call(
            f"""cd {element} && make all && sst-register {element} {element}_LIBDIR={os.getcwd()} && cd -""",
            shell=True
        )


def list_elems():

    subprocess.call("sst-register -l", shell=True)


parser = argparse.ArgumentParser(description="SST Element Installer")
parser.add_argument("--install", "-i", metavar="ELEMENT",
                    type=str, default="", help="Install element")
parser.add_argument("--uninstall", "-u", metavar="ELEMENT",
                    type=str, default="", help="Uninstall element")
parser.add_argument("--force", "-f", action="store_true", default=False)
parser.add_argument("--list", "-l", action="store_true", default=False)
parser.add_argument("--url", "-x", type=str,
                    default="https://github.com/sabbirahm3d/")

args = parser.parse_args()

if args.install and args.uninstall:
    print("no")
    exit(1)

if args.install:
    install(args.install, args.url, args.force)

if args.uninstall:
    uninstall(args.uninstall)

else:
    if args.list:
        list_elems()
