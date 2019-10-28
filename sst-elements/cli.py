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
                                     formatter_class=CustomHelpFormatter)

    _xor_parser = parser.add_mutually_exclusive_group()

    _xor_parser.add_argument("install", nargs="?", metavar="<ELEMENT>", type=str, default="",
                             help="Install element")
    _xor_parser.add_argument("--uninstall", "-u", metavar="<ELEMENT>", type=str, default="",
                             help="Uninstall element")
    _xor_parser.add_argument("--info", "-i", metavar="<ELEMENT>", type=str, default="",
                             help="Display element information")
    _xor_parser.add_argument("--list", "-l", action="store_true", default=False,
                             help="List all SST elements")
    _xor_parser.add_argument("--registered", "-r", action="store_true", default=False,
                             help="List elements registered to the system")
    parser.add_argument("--quiet", "-q", action="store_true", default=False,
                        help="Suppress standard outputs")
    parser.add_argument("--force", "-f", action="store_true", default=False,
                        help="Force installation")

    args = parser.parse_args().__dict__

    with open(os.devnull, "w") as devnull:

        if args["quiet"]:
            # suppress all console outputs
            sys.stdout = devnull

        if args["install"]:
            sstelements.install(args["install"], args["force"])

        elif args["uninstall"]:
            sstelements.uninstall(args["uninstall"])

        elif args["list"]:
            sstelements.pprint_all_elements()

        elif args["registered"]:
            print("\n".join(sstelements.list_registered_elements()))

        elif args["info"]:
            print("\n".join(sstelements.get_info(args["info"])))

        else:
            parser.print_help()
