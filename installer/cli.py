#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import installer


if __name__ == "__main__":

    class CustomHelpFormatter(argparse.RawDescriptionHelpFormatter):

        def __init__(self, prog):
            super().__init__(prog, max_help_position=40, width=100)

        def _format_action_invocation(self, action):
            if not action.option_strings or action.nargs == 0:
                return super()._format_action_invocation(action)
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
            return ", ".join(action.option_strings) + " " + args_string

    parser = argparse.ArgumentParser(description=installer.__doc__,
                                     formatter_class=CustomHelpFormatter, add_help=False)

    install_parser = parser.add_argument_group("Installation arguments")
    install_parser.add_argument("install", nargs="?", metavar="<ELEMENT>", type=str, default="",
                                help="Install element along with its dependencies.")
    install_parser.add_argument("--uninstall", "-u", metavar="<ELEMENT>", type=str, default="",
                                help="Uninstall element.")

    # build options
    install_parser.add_argument("--gen", "-g", nargs="?", metavar="Makefile|Ninja", type=str,
                                default="Makefile",
                                help="""Generator to build element.
                                Argument is case insensitive. (default: %(default)s)""")
    install_parser.add_argument("--jobs", "-j", nargs="?", metavar="<JOBS>", type=int, default=1,
                                help="""Maximum number of parallel builds.""")
    install_parser.add_argument("--dump", "-d", action="store_false", default=True,
                                help="Dump logs captured during the installation process.")

    # download options
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
    info_parser.add_argument("--dep", "-p", metavar="<ELEMENT>", type=str, default="",
                             help="Display dependencies of element")
    info_parser.add_argument("--tests", "-t", metavar="<ELEMENT>", type=str, default="",
                             help="Display tests on element")

    option_parser = parser.add_argument_group("Optional arguments")
    option_parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                               help="Show this help message and exit")
    option_parser.add_argument("-v", "--version", action="version",
                               version=installer.get_version(),
                               help="Show version number and exit")
    option_parser.add_argument("--quiet", "-q", action="store_true", default=False,
                               help="Suppress standard outputs")

    args = parser.parse_args().__dict__

    if args["quiet"]:
        # suppress all console outputs
        installer.LOG = False

    try:
        if args["install"]:
            installer.install(
                element=args["install"],
                generator=args["gen"].lower(),
                n_jobs=args["jobs"],
                force=args["force"],
                branch=args["branch"],
                commit=args["commit"],
                suppress_dump=args["dump"]
            )

        elif args["uninstall"]:
            installer.uninstall(args["uninstall"], args["force"])

        elif args["dep"]:
            dep = installer.get_dependencies(args["dep"])
            print("\n".join(dep) if dep else None)

        elif args["list"]:
            all_elements = installer.list_all_elements().keys()
            print("SST Elements".ljust(25), "Registered")
            print("-" * 41)
            for element in all_elements:
                if installer.is_registered(element):
                    # print check mark (✓)
                    print(f"{element.ljust(28)} \033[32m✓\033[0m")
                else:
                    print(element)

        elif args["registered"]:
            if args["registered"] == "all":
                print("\n".join(installer.list_registered_elements()))
            else:
                print(installer.is_registered(args["registered"]))

        elif args["info"]:
            print("\n".join(installer.get_info(args["info"])))

        elif args["tests"]:
            test_list = installer.list_tests(args["tests"])
            if test_list:
                print("\n".join(i.name for i in test_list))

        else:
            parser.print_help()

    except Exception as exc:
        raise SystemExit(exc) from None
