#!/usr/bin/env python

"""
Script to extract the Exposure value from an image overlay and create
a simple metadata file with a single line:

e.g.

exposure=20

If the metadata file already exists then just exit.  
"""

import os
import grp
import sys
import argparse

import stardot_overlay
from stardot_overlay import stardot_overlay as so


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=(
        "Create a metadata file with the exposure value extracted " +
        "from a StarDot camera image overlay."))

    # add command options
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true",
                        default=False)

    parser.add_argument("-n", "--dry-run",
                        help="extract exposure but don't write metafile",
                        action="store_true",
                        default=False)

    # add positional arguments
    parser.add_argument("file",
                        nargs='+',
                        help="StarDot Image File(s)")
    
    args = parser.parse_args()
    verbose = args.verbose
    dryrun = args.dry_run
    inlist = args.file

    if verbose:
        print("Verbose: {}".format(verbose))
        print("Dryrun: {}".format(dryrun))
        print("File list:")
        for file in inlist:
            print(file)

    # get user-id
    uid = os.getuid()
    
    # get nogroup group id for setting ownership
    groupinfo = grp.getgrnam("nogroup")
    gid = groupinfo[2]
    
    for inpath in inlist:
        
        # parse filename parts and construct metadata file name
        dname = os.path.dirname(inpath)
        fname = os.path.basename(inpath)
        fbase, fext = os.path.splitext(fname)
        mname = fbase + ".meta"
        mpath = os.path.join(dname, mname)
        if verbose:
            print("Dirname: {}".format(dname))
            print("Image File: {}".format(fname))
            print("Metadata File: {}".format(mname))

   
        if os.path.exists(mpath):
            if verbose:
                sys.stdout.write("Metadata file already exists.  Skipping.\n")
            continue
        
        try:
            exposure = int(so.get_exposure(inpath))
        except Exception:
            sys.stderr.write("Error extracting exposure " +
                             "for {}\n".format(inpath))
            header_lines = so.get_header_contents(inpath)
            print(header_lines)
            continue
        
        if verbose:
            print("Exposure: {}".format(exposure))

        if not dryrun:
            with open(mpath, 'w') as f:
                f.write("exposure={}\n".format(exposure))

            if uid == 0:
                os.chown(mpath, uid, gid)

    
    
