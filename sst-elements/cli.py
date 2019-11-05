#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

import sstelements


if __name__ == "__main__":

    class CustomHelpFormatter(argparse.HelpFormatter):

        def __init__(self, prog):
            super().__init__(prog, max_help_position=40, width=80)

        def _format_action_invocation(self, action):
            if not action.option_strings or action.nargs == 0:
                return super()._format_action_invocation(action)
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            return ", ".join(action.option_strings) + " " + args_string

    parser = argparse.ArgumentParser(description="SST Element Installer",
                                     formatter_class=CustomHelpFormatter, add_help=False)

    parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                        help="Show this help message and exit")
    parser.add_argument("-v", "--version", action="version",
                        version=sstelements.get_version(), help="Show version number and exit")
    parser._positionals.title = "Positional arguments"
    parser._optionals.title = "Optional arguments"
    _xor_parser = parser.add_mutually_exclusive_group()

    _xor_parser.add_argument("install", nargs="?", metavar="<ELEMENT>", type=str, default="",
                             help="Install element")
    _xor_parser.add_argument("--uninstall", "-u", metavar="<ELEMENT>", type=str, default="",
                             help="Uninstall element")
    _xor_parser.add_argument("--info", "-i", metavar="<ELEMENT>", type=str, default="",
                             help="Display information on element")
    _xor_parser.add_argument("--dep", "-d", metavar="<ELEMENT>", type=str, default="",
                             help="Display dependencies of element")
    _xor_parser.add_argument("--list", "-l", action="store_true", default=False,
                             help="List all SST elements")
    _xor_parser.add_argument("--registered", "-r", nargs="?", metavar="all|<ELEMENT>", type=str,
                             const="all", help="List elements registered to the system")
    parser.add_argument("--quiet", "-q", action="store_true", default=False,
                        help="Suppress standard outputs")
    parser.add_argument("--force", "-f", action="store_true", default=False,
                        help="Force installation")

    args = parser.parse_args().__dict__

    with open(os.devnull, "w") as devnull:

        if args["quiet"]:
            # suppress all console outputs
            sys.stdout = devnull

        try:
            if args["install"]:
                sstelements.install(args["install"], args["force"])

            elif args["uninstall"]:
                sstelements.uninstall(args["uninstall"])

            elif args["dep"]:
                dep = sstelements.get_dependencies(args["dep"])
                print("\n".join(dep) if dep else None)

            elif args["list"]:
                # sstelements.pprint_all_elements()
                all_elements = sstelements.list_all_elements().keys()
                print("SST Elements".ljust(25), "Registered")
                print("-" * 41)
                for element in all_elements:
                    if sstelements.is_registered(element):
                        # print check mark (✓)
                        print(element.ljust(28), "\033[32m✓\033[0m")
                    else:
                        print(element)

            elif args["registered"]:
                if args["registered"] == "all":
                    print("\n".join(sstelements.list_registered_elements()))
                else:
                    print(sstelements.is_registered(args["registered"]))

            elif args["info"]:
                print("\n".join(sstelements.get_info(args["info"])))

            else:
                parser.print_help()

        except Exception as exc:
            raise SystemExit(exc)
