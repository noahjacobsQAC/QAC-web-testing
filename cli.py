# -*- coding: utf-8 -*-

# python3 cli.py -u https://qaconsultants.com/ -n 1

import argparse
from src.scrapper.scrap import Scrap
from main import main

def sanityCheck(args):

    import requests
    from urllib.parse import urlparse

    if not Scrap.checkUrlValid(args.url):
        raise requests.ConnectionError(f"invalid url {args.url}")

    if args.navdepth < -1:
        raise OverflowError("depth range should be [-1, ... ).")

    main(args=args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='commands line arguments to scrap a url')

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="url to parse"
    )

    parser.add_argument(
        "-d",
        "--driver",
        type=str,
        required=False,
        default="Chrome",
        choices=["Chrome",'Firefox'],
        help="selenium driver to use"
    )

    parser.add_argument(
        "-tp",
        "--targetplatform",
        type=str,
        required=False,
        default="Desktop",
        choices=["Desktop",'Android','iOS'],
        help="device platform"
    )

    parser.add_argument(
        "-D",
        "--device",
        type=str,
        required=False,
        default=None,
        choices=["iPhone-X", "Google Nexus 5"],
        help="if device platform, which device to emulate"
    )

    parser.add_argument(
        "-n",
        "--navdepth",
        type=int,
        required=False,
        default=1,
        metavar="[ 0 ... )",
        help="webpage (nav) depth to itereate ( 0 full website )"
    )

    args = parser.parse_args()
    sanityCheck(args=args)


