#!/usr/bin/env python

"""
Script to extract the Exposure value from an image overlay.
"""

import os
import sys
import argparse

import stardot_overlay
from stardot_overlay import stardot_overlay as so


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=(
        "Extract the exposure value from a StarDot camera image " +
        "overlay."))

    # add command options
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true",
                        default=False)

    # add positional arguments
    parser.add_argument("filename",
                        help="StarDot Image File")
    
    args = parser.parse_args()
    verbose = args.verbose
    infile = args.filename

    if verbose:
        print("Filename: {}".format(infile))

        
    exposure = so.get_exposure(infile)
    print(exposure)
