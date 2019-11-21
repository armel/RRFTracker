#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import re

def main():

    # Lecture du fichier de test
    data = [line.strip() for line in open('../data/whois.cap')]
    pattern = '\(([^)]+)\) ([^)]+) (H|V|U|R|T10M|T6M|T|10M|6M)'
    whois = {}

    print 'Indicatif' + ';' + 'Prenom' + ';' + 'Type' + ';' + 'Description' + ';' + 'Tone' + ';' + 'Sysop' + ';' + 'Locator'
        
    # Boucle principale
    for line in data:
        whois.clear()
        tmp = line.split(';')

        whois['Indicatif'] = tmp[0].strip()
        whois['Type'] = tmp[1].strip()
        whois['Description'] = tmp[2].strip()
        whois['Tone'] = tmp[3].strip()
        whois['Locator'] = tmp[4].strip()

        if whois['Type'] == 'Hotspot':
            whois['Sysop'] = ''    
            if len(tmp) == 6:
                whois['Prenom'] = tmp[5].strip()
        else:
            whois['Prenom'] = ''    
            if len(tmp) == 6:
                whois['Sysop'] = tmp[5].strip()
            else:
                check = re.match(pattern, whois['Indicatif'])
                if check:
                    whois['Sysop'] = check.groups()[1].strip()

        if len(whois) == 7:
            print whois['Indicatif'] + ';' + whois['Prenom'] + ';' + whois['Type'] + ';' + whois['Description'] + ';' + whois['Tone'] + ';' + whois['Sysop'] + ';' + whois['Locator']


if __name__ == '__main__':
    main()