#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def main():

    indicatif = {}

    # Lecture des fichiers

    for i in ['12.dat', '01.dat', '02.dat']:

        data = [line.strip() for line in open(i)]

        for line in data:
            tmp = line[:-2]
            try:
                indicatif[tmp] += 1
            except:
                indicatif[tmp] = 1

    tmp = sorted(indicatif.items(), key=lambda x: x[1])
    tmp = reversed(tmp)

    for (l, t) in tmp:
        if t == 3:
            print l

if __name__ == '__main__':
    main()