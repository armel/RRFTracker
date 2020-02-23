#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

def main():

    # Lecture du fichier kml converti en csv
    kml = [line.strip() for line in open('rrf.csv')]

    # Lecture du fichier de web
    web = [line.strip() for line in open('rrf.web')]

    print'Indicatif;Prenom;Type;Description;Tone;Locator;Sysop;Longitude;Latitude'

    # Fabrication paire indicatif / lattitude et longitude

    indicatif = {}
    for line in kml:
        tmp = line.split(';')
        indicatif[tmp[0]] = tmp[3] + ';' + tmp[4]

    # Boucle principale
    for line in web:
        line = line.replace('tone', 'Tone')
        line = line.replace('MHZ', 'MHz')
        line = line.replace('HZ', 'Hz')

        tmp = line.split('\t')
        tmpbis = tmp[2].split('Tone')

        if len(tmp) == 4:
            tmp[2] = tmp[2].replace('tone', 'Tone')
            tmpbis = tmp[2].split('Tone')
            result = tmp[0].strip() + ';;' + tmp[1].strip() + ';' + tmpbis[0].strip() + ';' + tmpbis[1].strip() + ';' +  tmp[3].strip() + ';' 
        elif len(tmp) == 5:
            result = tmp[0].strip() + ';;' + tmp[1].strip() + ';' + tmpbis[0].strip() + ';' + tmpbis[1].strip() + ';' +  tmp[3].strip() + ';' +  tmp[4].strip()

        if tmp[0].strip() in indicatif:
            result += ';' + indicatif[tmp[0].strip()]

        print result
if __name__ == '__main__':
    main()
