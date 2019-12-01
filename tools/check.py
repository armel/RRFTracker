#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

def main():

    # Lecture du fichier de test
    data = [line.strip() for line in open('../data/whois.dat')]

    # Boucle principale
    for line in data:
        tmp = line.split(';')
        if len(tmp) == 7:
            print tmp
        else:
            print 'Error'
            
if __name__ == '__main__':
    main()