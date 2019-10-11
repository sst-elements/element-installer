#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import sstelements

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SST Element Installer")
    parser.add_argument("--install", "-i", metavar="ELEMENT", type=str, default="",
                        help="Install element")
    parser.add_argument("--uninstall", "-u", metavar="ELEMENT", type=str, default="",
                        help="Uninstall element")
    parser.add_argument("--quiet", "-q", action="store_true", default=False,
                        help="Supress standard outputs")
    parser.add_argument("--force", "-f", action="store_true", default=False,
                        help="Force installation")
    parser.add_argument("--list", "-l", action="store_true", default=False,
                        help="List all elements")
    parser.add_argument("--registered", "-r", action="store_true", default=False,
                        help="List registered elements")
    parser.add_argument("--url", "-x", type=str, default="sabbirahm3d",
                        help="External URL for element")
    parser.add_argument("--details", "-d", metavar="ELEMENT", type=str, default="",
                        help="Display element information")

    args = parser.parse_args().__dict__

    with open(os.devnull, "w") as devnull:
        if args["quiet"]:
            # suppress all console outputs
            sys.stdout = devnull

        # install and uninstall options are mutually exclusive
        if args["install"] and args["uninstall"]:
            parser.print_help()
            exit(1)

        elif args["install"]:
            sstelements.install(args["install"], args["url"], args["force"])

        elif args["uninstall"]:
            sstelements.uninstall(args["uninstall"])

        elif args["list"]:
            sstelements.pprint_all_elements()

        elif args["registered"]:
            print("\n".join(sstelements.list_registered_elements()))

        elif args["details"]:
            print(sstelements.get_info(args["details"]))

        else:
            parser.print_help()
