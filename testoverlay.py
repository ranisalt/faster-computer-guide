#!/usr/bin/env python

from __future__ import print_function
import platform
import os
import sys

def main():
    release = platform.release()

    bootfile, procfile = '/boot/config-%s' % release, '/proc/config.gz'

    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        print('Config found at supplied file')
        openf, filename = open, sys.argv[1]

    elif os.path.isfile(bootfile):
        print('Config found at %s' % bootfile)
        openf, filename = open, bootfile

    elif os.path.isfile(procfile):
        import gzip

        print('Config found at %s' % procfile)
        openf, filename = gzip.open, procfile

    else:
        print('Config not found!')
        return

    with openf(filename) as config:
        # assuming config file was not edited manually, as kernel config
        # helpers write "# CONFIG_OVERLAY_FS is not set" when disabled
        haystack = config.read()
        if isinstance(haystack, bytes):
            haystack = haystack.decode()

        if 'CONFIG_OVERLAY_FS=' in haystack:
            print('overlayfs is available :)')
        else:
            print('overlayfs is not available :(')


if __name__ == '__main__':
    main()

