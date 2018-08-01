# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         FirstLast_2.0.py
# Purpose:      Mark 2 for FirstLast.py to test intervallic relationships in Danse
#               de la Fureur.
#
# Authors:      Luke Poeppel
#
# Copyright:    Copyright © 2006-2016 Michael Scott Cuthbert and the music21 Project
# Licence:      LGPL or BSD, see licence.txt
#-------------------------------------------------------------------------------
'''
In Olivier Messiaen's, Danse de la Fureur (sixth movement in his chamber work, Le Quatuor pour la 
Fin du Temps), certain intervallic relationships between the first and last notes of each measure
appear more frequently than others. This program investigates which intervals (between first and last pitch
values of each measures) occur most frequently and uses p-value testing to see whether or not this 
was an intentional motive of Messian.

New Result with fixed data: 
1.9%... bad?
'''

from __future__ import division, print_function

import random

from music21 import converter
from music21 import note
from music21 import stream

danse = converter.parse('/Users/lukepoeppel/Dropbox/Luke_Myke/Messiaen_Qt/Messiaen_VI_Danse/Danse_de_la_fureur.xml')

danse_instrument = danse.parts[0]

runRandom = True

runFalseValue = 65.1685393259

def getFirstLastIndex(numNotesInMeasure):
    '''
    Based on whether or not the program is running on runRandom (choosing random index values for the measure)
    returns the indices to be chosen for each measure.
    '''
    if not runRandom:
        return (0, -1)

    firstIndex = 0
    lastIndex = 0

    while firstIndex == lastIndex:
        firstIndex = random.randint(0, (numNotesInMeasure - 1))
        lastIndex = random.randint(0, (numNotesInMeasure - 1))

    return (firstIndex, lastIndex)

measureMap = {}

def getIntervalFirstLast(measureNumber, thisMeasure):
    '''
    Returns the int(pitch.ps) distance between the first and last notes of each measure.
    '''
    notes = []

    if measureNumber not in measureMap:
        measureMap[measureNumber] = thisMeasure.stripTies().flat.getElementsByClass(note.Note)

    flattened = measureMap[measureNumber]

    for thisNote in flattened:
        notes.append(thisNote)

    numNotesInMeasure = len(notes)

    if numNotesInMeasure < 2:
        return None

    (firstIndex, lastIndex) = getFirstLastIndex(numNotesInMeasure)

    try:
        first = int(notes[firstIndex].pitch.ps)
        last = int(notes[lastIndex].pitch.ps)
    except IndexError:
        return None

    intervalFirstLast = abs(last - first) % 12

    return intervalFirstLast

def runOnce(danse_instrument):
    intervals = []

    for measureNumber, thisMeasure in enumerate(danse_instrument.getElementsByClass(stream.Measure)):
        intervalFirstLast = getIntervalFirstLast(measureNumber, thisMeasure)

        if intervalFirstLast is None:
            continue

        intervals.append(intervalFirstLast)

    unison = intervals.count(0)
    percentageOfUnison = (unison / 89) * 100

    major2 = intervals.count(2)
    percentageOfMajor2 = (major2 / 89) * 100

    major3 = intervals.count(4)
    percentageOfMajor3 = (major3 / 89) * 100

    tritone = intervals.count(6)
    percentageOfTritone = (tritone / 89) * 100

    isTrueValue = (percentageOfUnison + percentageOfMajor2 + percentageOfMajor3 + percentageOfTritone)

    if isTrueValue > runFalseValue:
        print('')
        print('UNISON: ' + str(percentageOfUnison))
        print('MAJOR 2: ' + str(percentageOfMajor2))
        print('MAJOR 3: ' + str(percentageOfMajor3))
        print('TRITONE: ' + str(percentageOfTritone))
        print('------------------------------')
        print(isTrueValue)

    if i % 20 == 0:
        print(i)

numberOfTimesToRun = 1000

if not runRandom:
    numberOfTimesToRun = 1

for i in range(numberOfTimesToRun):
    runOnce(danse_instrument)