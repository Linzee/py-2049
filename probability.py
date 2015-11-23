#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time

def findItems(path, trains):
    items = []
    with open(path) as file:
        for line in file:
            try:
                item = json.loads(line)
                processedItem = processItem(items, trains, item)
                if processedItem:
                    items.append(processedItem)
            except ValueError:
                print("Invalid JSON line! (" + line + ")")
    return items

def processItem(items, trains, item):
    
    if item['name'] not in trains:
        return
    
    return item

def findStations(trains, items):
    
    equalStations = loadEqualStations()
    
    stations = []
    
    for i in range(0, len(trains) - 1):
        thisTrain = trains[i]
        thatTrain = trains[i + 1]
        station = findStationForTrains(thisTrain, thatTrain, items, equalStations)
        if station:
            stations.append(station)
        else:
            return None

    return stations

def findStationForTrains(thisTrain, thatTrain, items, equalStations):
    
    thisTrainStations = findAllStationForTrain(thisTrain, items)
    thatTrainStations = findAllStationForTrain(thatTrain, items)
    
    for thisStation in thisTrainStations:
        thisStationAndEqual = getStationAndEqual(thisStation, equalStations)
        for thatStation in thatTrainStations:
            if thatStation in thisStationAndEqual:
                return thisStation
    
    print "Found no station for trains ", thisTrain, thatTrain
    return None

def getStationAndEqual(station, equalStations):
    
    if station in equalStations:
        return equalStations[station]
    else:
        list = []
        list.append(station)
        return list

def findAllStationForTrain(train, items):
    stations = []
    
    for item in items:
        if item['name'] == train:
            if item['station'] not in stations:
                stations.append(item['station'])

    if len(stations) is 0:
        print "Found no stations for train", train

    return stations

def loadEqualStations():
    
    euqalStations = {}
    path = 'equalStations.json'
    
    with open(path) as file:
        for line in file:
            try:
                stations = json.loads(line)
                for station in stations:
                    stationList = stations[station]
                    
                    if station not in euqalStations:
                        euqalStations[station] = []
                    
                    for s in stationList:
                        euqalStations[station].append(s)
                    
            except ValueError:
                print("Invalid JSON line! (" + line + ")")
                
    return euqalStations

def calculateProbability(trains, maxDelays, stations, items, index):
    
    allItems = 0
    someItems = 0

    train = trains[index]
    station = stations[index]
    maxDelay = int(maxDelays[index])

    for item in items:
        if item['name'] == train and item['station'] == station:
            allItems += 1
            if int(item['delay']) < maxDelay:
                someItems += 1

    prob = float(someItems) / float(allItems)

    return prob, someItems, allItems

def probability(dataPath, optionsValues):
    
    print
    
    i = 0
    trains = []
    maxDelays = []
    while i < len(optionsValues):
        trains.append(optionsValues[i])
        if(i + 1 < len(optionsValues)):
            maxDelays.append(optionsValues[i + 1])
        i += 2
    
    items = findItems(dataPath, trains)
    stations = findStations(trains, items)
    
    if stations:
        
        tprob = 1.0
        
        for i in range(0, len(trains) - 1):
            
            fromStation = ""
            if i-1 >= 0:
                fromStation = stations[i-1]
            
            toStation = ""
            if i < len(stations):
                toStation = stations[i]
            
            maxDelay = ""
            if i < len(maxDelays):
                maxDelay = str(maxDelays[i])
            
            prob, someItems, allItems = calculateProbability(trains, maxDelays, stations, items, i)
            
            sts = 'max ' + str(maxDelay) + 'min. ' + str(someItems) + '/' + str(allItems)
            
            print fromStation.ljust(26, ' '), '>', toStation.rjust(26, ' ')
            print trains[i].ljust(26, ' '), ' ', sts.rjust(26, ' ')
            print "%.0f%%" % (100 * prob)
            print (26 * 2 + 3) * '-'
            
            tprob *= prob
            
        print
        print "Pravdeopdobnost ze stihnes prestupit je", "%.0f%%" % (100 * tprob)
    else:
        print("No path found!")
    
#python 2049.py -p "EC 277 Slovan" 40 "R 1601 Chopok" 10 "Os 9119" 20 "Os 9219"
#python 2049.py -p "Os 9206" 5 "Os 8769" 20 "R 606 shoppie.sk" 5 "EC 274 Jaroslav Hašek"