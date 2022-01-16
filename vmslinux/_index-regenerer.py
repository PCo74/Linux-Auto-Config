#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
regénère «index.html»
avec actualisation de la liste des machines Linux disponibles
©PCo/2015-2021
"""

import glob
import os
from datetime import date

FIC_INDEX = "index.html"
FIC_BASE = "_index_base.html"
FIC_CONFIG = "../config.ini"

def exporterListe(unNom, uneListe):
    contenu = unNom + "=(\n"
    for item in uneListe:
        contenu += item + "\n"
    contenu += ")\n"
    return contenu

def obtenirMachines():
    vms = []
    for filtre in ["./[!_]*.txt", "./[!_]*/*.txt"]:
        for i, fictxt in enumerate(glob.glob(filtre)):
            fictxt = fictxt.replace("\\", "/")[2:] # cf. Windows
            vms.append(os.path.splitext(fictxt)[0])
    return vms

# REF : https://stackoverflow.com/questions/3595363/properties-file-in-python-similar-to-java-properties
def loadProperties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value 
    return props

#### main

props = loadProperties(FIC_CONFIG)
machines = obtenirMachines()
print("\nListe des VMs\n" + "-"*61)
print(*machines, sep="\n")
print("-"*61, "\n")

entete="""#!/bin/bash

#<meta charset="UTF-8">
#<style>h1 {{color: maroon;}} pre {{tab-size: 4;}} </style>
#<h1>Linux-Auto-Configuration ©PCo/2016-2021</h1>

#<pre>
set -e

IDFIC="{}"
IP="{}"
PORT="{}"

""".format(props['IDFIC'],props['IP'],props['PORT'])

with open(FIC_INDEX, 'wb') as f:
    f.write(entete.encode())
    maintenant = date.today().strftime("%Y/%m/%d")
    f.write(("# liste des VMs au "+maintenant+"\n").encode())
    contenu = exporterListe("vms", machines)        
    f.write(contenu.encode())
    with open(FIC_BASE, 'rb') as fbase:
        f.write(fbase.read())
    f.write("#</pre>".encode())
