#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import re

def main():

    # Lecture du fichier de test
    data = [line.strip() for line in open('whois.dat')]

    # Boucle principale
    for line in data:
        tmp = line.split(';')
        if len(tmp) == 9:
            tone = tmp[3].split(' ')
            value = re.findall(r"[-+]?\d*\.\d+|\d+", tone[0])
            reverse = ''
            if len(value) == 1:
                reverse = str(value[0]) + ' Hz'

            if reverse != tmp[3]:
                print '-----> Error 1 : ', line, reverse, tmp[3]

        else:
            print '-----> Error 2 : ', line
            
if __name__ == '__main__':
    main()