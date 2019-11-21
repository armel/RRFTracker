#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

def main():

    # Lecture du fichier de test
    data = [line.strip() for line in open('../data/whois.web')]

    # Boucle principale
    for line in data:
        line = line.replace('tone', 'Tone')
        line = line.replace('MHZ', 'MHz')
        line = line.replace('HZ', 'Hz')

        tmp = line.split('\t')
        tmpbis = tmp[2].split('Tone')

        if len(tmp) == 4:
            tmp[2] = tmp[2].replace('tone', 'Tone')
            tmpbis = tmp[2].split('Tone')
            print tmp[0].strip() + ';' + tmp[1].strip() + ';' + tmpbis[0].strip() + ';' + tmpbis[1].strip() + ';' +  tmp[3].strip() 
        elif len(tmp) == 5:
            print tmp[0].strip() + ';' + tmp[1].strip() + ';' + tmpbis[0].strip() + ';' + tmpbis[1].strip() + ';' +  tmp[3].strip() + ';' +  tmp[4].strip()            
if __name__ == '__main__':
    main()