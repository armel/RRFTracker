#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time

upper = 'ABCDEFGHIJKLMNOPQRSTUVWX'
lower = 'abcdefghijklmnopqrstuvwx'

# Compute locator
# https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square
def to_grid(dec_lat, dec_lon):
    if not (-180<=dec_lon<180):
        sys.stderr.write('longitude must be -180<=lon<180, given %f\n'%dec_lon)
        sys.exit(32)
    if not (-90<=dec_lat<90):
        sys.stderr.write('latitude must be -90<=lat<90, given %f\n'%dec_lat)
        sys.exit(33) # can't handle north pole, sorry, [A-R]

    adj_lat = dec_lat + 90.0
    adj_lon = dec_lon + 180.0

    grid_lat_sq = upper[int(adj_lat/10)];
    grid_lon_sq = upper[int(adj_lon/20)];

    grid_lat_field = str(int(adj_lat%10))
    grid_lon_field = str(int((adj_lon/2)%10))

    adj_lat_remainder = (adj_lat - int(adj_lat)) * 60
    adj_lon_remainder = ((adj_lon) - int(adj_lon/2)*2) * 60

    grid_lat_subsq = lower[int(adj_lat_remainder/2.5)]
    grid_lon_subsq = lower[int(adj_lon_remainder/5)]

    return grid_lon_sq + grid_lat_sq + grid_lon_field + grid_lat_field + grid_lon_subsq + grid_lat_subsq

def main():
    error = []

    # Lecture du fichier kml converti en csv
    # https://www.convertcsv.com/kml-to-csv.htm
    kml = [line.strip() for line in open('rrf.csv')]

    # Lecture du fichier annuaire
    anu = [line.strip() for line in open('annuaire.csv')]

    print'Indicatif;Type;Description;Tone;Locator;Longitude;Latitude;Sysop;Prenom'

    # Fabrication paire indicatif / lattitude et longitude

    geoloc = {}
    for line in kml:
        tmp = line.split(';')
        geoloc[tmp[0]] = tmp[3] + ';' + tmp[4]

    prenoms = {}
    for line in anu:
        tmp = line.split(';')
        prenoms[tmp[0]] = tmp[2][0] + tmp[2][1:].lower()

    # Boucle principale
    for line in kml:
        line = line.replace('tone', 'Tone')
        line = line.replace('MHZ', 'MHz')
        line = line.replace('HZ', 'Hz')

        if '?' in line:
            continue

        tmp = line.split(';')

        indicatif = tmp[0].strip()
        type = indicatif[-1:]
        if type == 'H':
            type = 'Hotspot'
        elif type in ['R']:
            type = 'Relais'
        elif 'T' in type:
            type = 'Transpondeur'
        elif type in ['U', 'V']:
            type = 'Link'
        elif '-' in tmp[1]:
            type = 'Relais'
        else:
            type = 'Link' 

        longitude = tmp[3].strip()
        latitude = tmp[4].strip()
        locator = to_grid(float(latitude), float(longitude))

        a = tmp[1]

        a = a.split('<br>')
        b = a[0].split('Tone')

        try:
            if len(a) > 1:
                description = b[0].strip()
                tone = b[1].strip()
                sysop = a[1].strip()
            else:
                description = b[0].strip()
                tone = b[1].strip()
                sysop = ''
        except:
            error.append(line)


        if sysop !='' :
            try:
                prenom = prenoms[sysop]
            except:
                prenom = ''
        else:
            tmp = indicatif.split(' ')
            try:
                prenom = prenoms[tmp[1]]
            except:
                prenom = ''
            '''
            if type == 'Hotspot':
                tmp = indicatif.split(' ')
                try:
                    prenom = prenoms[tmp[1]]
                except:
                    prenom = ''
            else:
                prenom = ''
            '''

        result = indicatif + ';' + type + ';' + description + ';' + tone + ';' + locator + ';' + longitude + ';' + latitude + ';' + sysop + ';' + prenom

        print result
    
    if error:
        print '----------'
        for e in error:
            print e
if __name__ == '__main__':
    main()
