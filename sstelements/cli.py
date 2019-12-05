#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import sstelements


if __name__ == "__main__":

    class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):

        def __init__(self, prog):
            super().__init__(prog, max_help_position=40, width=80)

        def _format_action_invocation(self, action):
            if not action.option_strings or action.nargs == 0:
                return super()._format_action_invocation(action)
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            return ", ".join(action.option_strings) + " " + args_string

    parser = argparse.ArgumentParser(description=sstelements.__doc__,
                                     formatter_class=CustomHelpFormatter, add_help=False)

    install_parser = parser.add_argument_group("Installation arguments")
    install_parser.add_argument("install", nargs="?", metavar="<ELEMENT>", type=str, default="",
                                help="Install element along with its dependencies")
    install_parser.add_argument("--uninstall", "-u", metavar="<ELEMENT>", type=str, default="",
                                help="Uninstall element")
    install_parser.add_argument("--branch", "-b", metavar="<BRANCH>", type=str, default="master",
                                help="""Branch of element repository. By default, the installer
                                 will clone the master branch of the element's repository.""")
    install_parser.add_argument("--commit", "-c", metavar="<SHA>", type=str, default="",
                                help="""Commit SHA of element repository. By default, the installer
                                 will clone the version of the repository at its head.""")
    install_parser.add_argument("--force", "-f", action="store_true", default=False,
                                help="""Flag to force installation or removal of element.
                        If option is applied to installation, the existing files will be
                        overwritten by the updated versions.
                        If option is applied to uninstallation, the element as well as all its
                        dependent elements will be removed.""")

    info_parser = parser.add_argument_group("Element information arguments")
    info_parser.add_argument("--list", "-l", action="store_true", default=False,
                             help="List all SST elements")
    info_parser.add_argument("--registered", "-r", nargs="?", metavar="all|<ELEMENT>", type=str,
                             const="all", help="List elements registered to the system")
    info_parser.add_argument("--info", "-i", metavar="<ELEMENT>", type=str, default="",
                             help="Display information on element")
    info_parser.add_argument("--dep", "-d", metavar="<ELEMENT>", type=str, default="",
                             help="Display dependencies of element")

    option_parser = parser.add_argument_group("Optional arguments")
    option_parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                               help="Show this help message and exit")
    option_parser.add_argument("-v", "--version", action="version",
                               version=sstelements.get_version(),
                               help="Show version number and exit")
    option_parser.add_argument("--quiet", "-q", action="store_true", default=False,
                               help="Suppress standard outputs")

    args = parser.parse_args().__dict__

    if args["quiet"]:
        # suppress all console outputs
        sstelements.LOG = False

    try:
        if args["install"]:
            sstelements.install(args["install"], args["force"], args["branch"], args["commit"])

        elif args["uninstall"]:
            sstelements.uninstall(args["uninstall"], args["force"])

        elif args["dep"]:
            dep = sstelements.get_dependencies(args["dep"])
            print("\n".join(dep) if dep else None)

        elif args["list"]:
            all_elements = sstelements.list_all_elements().keys()
            print("SST Elements".ljust(25), "Registered")
            print("-" * 41)
            for element in all_elements:
                if sstelements.is_registered(element):
                    # print check mark (✓)
                    print(f"{element.ljust(28)} \033[32m✓\033[0m")
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
        raise SystemExit(exc) from None