#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
génère vue des vmslinux
©PCo-2017
"""

import glob
import sys
import os
from os.path import basename
import re
import html
import webbrowser

IDFIC="=--="

def debut(unNomVM):
    global schema
    img_schema = ""
    if schema:
        img_schema = """
        <p>
          <img class="fixe" src="{0}.png" alt="schéma {0}">
        </p>""".format(schema)
    
    return """<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type">
    <title>{0}</title>
    <meta name="author" content="PCo-2016/2019">
    <meta name="description" content="SISR">
    <meta name="highlight" content="true">
    <meta name="pasnumero" content="false">
    <link rel="icon" href="http://cp.cosson.free.fr/pco-css-js/favicon.ico">
    <link rel="stylesheet" type="text/css" href="http://cp.cosson.free.fr/pco-css-js/cours.css">
    <script language="javascript" src="http://cp.cosson.free.fr/pco-css-js/dev_red_hx.js"></script>
    <style>
      i {{color: mediumaquamarine;}}
      pre {{tab-size: 4;-moz-tab-size: 4;}}
      b .hljs-comment {{color: red;}}
    </style>
  </head>
  <body>
      {1}
""".format(unNomVM, img_schema)       


def titreFichier(unType, unNom):
    return """

    <h1><i>{0}</i> {1}</h1>

    <pre><code class="bash">""".format(unType, unNom)


def finCode():
    return """</code></pre>"""


def fin():
    return """

    </body>
</html>"""    


def attention(uneLigne):
    return """# <b><strong>✋</strong>{0}</b>""".format(uneLigne)


def genererHTML(unFic):
    global fic_exceptions
    IDFIC_LG=len(IDFIC)
    sortie = False
    titre_fichier = "?"
    with open(unFic + '.html', 'w', -1, "utf-8") as fh:
        fh.write(debut(unFic))
        with open(unFic + '.txt', 'r', -1, "utf-8") as ft: 
            for ligne in ft:
                ligne = ligne.rstrip('\n\r')
                if ligne[:IDFIC_LG] == IDFIC:  # repère nom fichier
                    if sortie :
                        fh.write(finCode())    
                    sortie = estAffiche(ligne[IDFIC_LG:]) # afficher ou non !           
                    nom = ligne[IDFIC_LG:].split()[0]
                    if ligne[IDFIC_LG] == "/" or ligne[IDFIC_LG] == ".":
                        titre_fichier = titreFichier("$ nano", nom)
                    else:
                        titre_fichier = titreFichier("$ bash", nom)
                else:
                    if sortie :
                        if ligne[0:5] != "# !!!" :
                            ligne = html.escape(ligne).replace(chr(27), '␛')
                        else:
                            ligne = attention(ligne[5:])
                        if titre_fichier != "":
                            fh.write(titre_fichier + ligne)
                            #print(titre_fichier + ligne)
                            titre_fichier = ""
                        else:                     
                            fh.write("\n" + ligne)
                            #print("\n" + ligne)
            if sortie:
                fh.write(finCode())
            fh.write(fin())

def estAffiche(unFic):
    """ détermine si le fichier <unFic> est à afficher
        -> str unFic    un nom de fichier
        <- bool {True|False}
    """
    fic_exceptions = ( r"/etc/issue", r"_(.*)$" )
    for expreg in fic_exceptions:
        if re.match(expreg, unFic):
            return False
    return True

## MAIN


if len(sys.argv) < 2:  # fin du script
    sys.exit("""Argument manquant !
Syntaxe : 01-vmslinux-vue-html.py {répertoire|fichier .txt}""")
    
reffic = os.path.basename(sys.argv[1])
schema = None

if os.path.isfile(reffic):
    chemin = reffic
else:
    chemin = reffic + "/*.txt"
    if os.path.isfile(reffic + "/" + reffic + ".png"):
        schema = reffic

print(chemin, schema)

for fic in glob.glob("./" + chemin):
    fic = fic.replace("\\", "/")[2:]
    print(os.path.splitext(fic))
    print(os.path.splitext(fic)[0])
    genererHTML(os.path.splitext(fic)[0])
    path = os.path.abspath(__file__)
    path = os.path.dirname(path) + "/"
    url = "file://" + path + os.path.splitext(fic)[0] + ".html"
    print(url)
    webbrowser.open(url, new=2)
