#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 14:53:00 2020

@author: fatih
"""

import os
import subprocess
import sys
from shutil import rmtree
from pathlib import Path
import distro
from datetime import datetime
import apt
import random, string


def main():
    def update():
        try:
            cache = apt.Cache()
            cache.open()
            cache.update()
        except Exception as e:
            print(str(e))

    def subupdate():
        subprocess.call(["apt", "update"],
                        env={**os.environ, 'DEBIAN_FRONTEND': 'noninteractive'})

    def fixbroken():
        subprocess.call(["apt", "install", "--fix-broken", "-yq"],
                        env={**os.environ, 'DEBIAN_FRONTEND': 'noninteractive'})

    def dpkgconfigure():
        subprocess.call(["dpkg", "--configure", "-a"],
                        env={**os.environ, 'DEBIAN_FRONTEND': 'noninteractive'})

    def externalrepo(key, sources, name):
        tmpkeyfilename = ''.join(random.choice(string.ascii_lowercase) for i in range(13))
        tmpkeyfile = open(os.path.join("/tmp", tmpkeyfilename), "w")
        tmpkeyfile.write(key)
        tmpkeyfile.flush()
        tmpkeyfile.close()
        tmpkey = os.path.join("/tmp", tmpkeyfilename)

        subprocess.call(["apt-key", "add", tmpkey])

        Path("/etc/apt/sources.list.d/").mkdir(parents=True, exist_ok=True)
        sdfile = open("/etc/apt/sources.list.d/" + name, "w")
        sdfile.write(sources)
        sdfile.flush()
        sdfile.close()

        if os.path.isfile(tmpkey):
            os.remove(tmpkey)

    def correctsourceslist():
        found = True
        source = ""
        major = distro.major_version()
        codename = distro.codename().lower()
        now = datetime.now()

        if codename == "ondokuz":
            source = "### The Official Pardus Package Repositories ###\n\n" \
                     "deb http://depo.pardus.org.tr/pardus ondokuz main contrib non-free\n" \
                     "# deb-src http://depo.pardus.org.tr/pardus ondokuz main contrib non-free\n\n" \
                     "deb http://depo.pardus.org.tr/guvenlik ondokuz main contrib non-free\n" \
                     "# deb-src http://depo.pardus.org.tr/guvenlik ondokuz main contrib non-free\n\n" \
                     "### This section generated by Pardus Software at " + str(now) + " ###\n"
        elif codename == "yirmibir":
            source = "### The Official Pardus Package Repositories ###\n" \
                     "deb http://depo.pardus.org.tr/pardus yirmibir main contrib non-free\n" \
                     "# deb-src http://depo.pardus.org.tr/pardus yirmibir main contrib non-free\n\n" \
                     "deb http://depo.pardus.org.tr/guvenlik yirmibir main contrib non-free\n" \
                     "# deb-src http://depo.pardus.org.tr/guvenlik yirmibir main contrib non-free\n\n" \
                     "### This section generated by Pardus Software at " + str(now) + " ###\n"
        elif codename == "etap":
            if major == "19":
                source = "### The Official Pardus Package Repositories ###\n" \
                         "deb http://19.depo.pardus.org.tr/etap ondokuz main contrib non-free\n" \
                         "# deb-src http://19.depo.pardus.org.tr/etap ondokuz main contrib non-free\n\n" \
                         "deb http://19.depo.pardus.org.tr/etap-guvenlik ondokuz main contrib non-free\n" \
                         "# deb-src http://19.depo.pardus.org.tr/etap-guvenlik ondokuz main contrib non-free\n\n" \
                         "### This section generated by Pardus Software at " + str(now) + " ###\n"
            elif major == "21":
                source = "### The Official Pardus Package Repositories ###\n" \
                         "deb http://21.depo.pardus.org.tr/etap yirmibir main contrib non-free\n" \
                         "# deb-src http://21.depo.pardus.org.tr/etap yirmibir main contrib non-free\n\n" \
                         "deb http://21.depo.pardus.org.tr/etap-guvenlik yirmibir main contrib non-free\n" \
                         "# deb-src http://21.depo.pardus.org.tr/etap-guvenlik yirmibir main contrib non-free\n\n" \
                         "### This section generated by Pardus Software at " + str(now) + " ###\n"
            else:
                found = False
        else:
            found = False

        if found:
            rmtree("/etc/apt/sources.list.d", ignore_errors=True)
            Path("/etc/apt/sources.list.d").mkdir(parents=True, exist_ok=True)
            sfile = open("/etc/apt/sources.list", "w")
            sfile.write(source)
            sfile.flush()
            sfile.close()

    if len(sys.argv) > 1:
        if sys.argv[1] == "externalrepo":
            externalrepo(sys.argv[2], sys.argv[3], sys.argv[4])
            update()
        elif sys.argv[1] == "correctsourceslist":
            correctsourceslist()
        elif sys.argv[1] == "update":
            update()
        elif sys.argv[1] == "fixapt":
            correctsourceslist()
            subupdate()
            fixbroken()
            dpkgconfigure()
        else:
            print("unknown argument error")
    else:
        print("no argument passed")


if __name__ == "__main__":
    main()
