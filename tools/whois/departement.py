#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import re

def main():

    # Lecture du fichier de test
    data = [line.strip() for line in open('departement.dat')]

    # Boucle principale
    for line in data:
        tmp = line.split(',')
        print(tmp[0] + ';' + tmp[1])
            
if __name__ == '__main__':
    main()