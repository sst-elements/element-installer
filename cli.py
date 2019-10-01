#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import config
import install

if __name__ == "__main__":

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="SST Element Installer")
    parser.add_argument("--install", "-i", metavar="ELEMENT", type=str, default="",
                        help="Install element")
    parser.add_argument("--uninstall", "-u", metavar="ELEMENT", type=str, default="",
                        help="Uninstall element")
    parser.add_argument("--force", "-f", action="store_true", default=False)
    parser.add_argument("--list", "-l", action="store_true", default=False)
    parser.add_argument("--url", "-x", type=str, default=config.ELEMENT_REPO_URL)

    args: argparse.Namespace = parser.parse_args()

    # install and uninstall options are mutually exclusive
    if args.install and args.uninstall:
        parser.print_help()
        exit(1)

    elif args.install:
        install.install(args.install, args.url, args.force)

    elif args.uninstall:
        install.uninstall(args.uninstall)

    elif args.list:
        install.list_elems()

    else:
        parser.print_help()
