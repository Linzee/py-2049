#!/usr/bin/env python

import matplotlib.pyplot as plt
from statsOutput import Output
from datetime import datetime
import numpy as np
import pandas
import time
import json

def loadItems(path, options):
    output = Output()
    with open(path) as file:
        for line in file:
            item = None
            try:
                item = json.loads(line)
            except ValueError:
                print("Invalid JSON line! (" + line + ")")
            if item:
                processItem(output, options, item)
    return output

def processItem(output, options, item):

    if options.train:
        if options.train not in item['name']:
            return
    
    timestamp = time.mktime(time.strptime(item['time'], '%Y-%m-%d %H:%M:%S'))
    day = int(timestamp / (60 * 60 * 24))
    delay = int(item['delay'])
    
    item['delay'] = delay #fix data, delay have to by numeric
    item['day'] = day
    
    output.items.append(item)
    
    trainDayKey = str(day) + ":" + item['name'];
    if trainDayKey not in output.stats:
        output.stats[trainDayKey] = []
    output.stats[trainDayKey].append(delay)

def printStats(output):
    
    print('')
    print('Gobalne statistiky:')
    
    allDelays = []
    for someItems in output.stats.values():
        allDelays.extend(someItems)
    
    avg = np.mean(allDelays)
    sum = np.sum(allDelays)
    
    def minutes(mins):
        return str(int(round(mins))) + 'min.'
    
    print('Priemerne meskanie: ' + minutes(avg))
    print('Celkove meskanie: ' + minutes(sum))
    
    print('')
    print('Podla vlaku:')
    
    df = pandas.DataFrame(output.items)
    byTrain = df.groupby(df['name'])['delay']
    
    min = byTrain.min().reset_index().min()
    max = byTrain.max().reset_index().max()
    avgMin = byTrain.mean().reset_index().min()
    avgMax = byTrain.mean().reset_index().max()
    
    print('Najmensie meskanie: ' + min['name'] + ' (' + minutes(min['delay']) + ')')
    print('Najvecsie meskanie: ' + max['name'] + ' (' + minutes(max['delay']) + ')')
    print('Najmensie priemerne meskanie: ' + avgMin['name'] + ' (' + minutes(avgMin['delay']) + ')')
    print('Najvecsie priemerne meskanie: ' + avgMax['name'] + ' (' + minutes(avgMax['delay']) + ')')
    
    print('')
    print('Podla dni:')
    
    byDay = df.groupby(df['day'])['delay']
    
    min = byDay.min().reset_index().min()
    max = byDay.max().reset_index().max()
    avgMin = byDay.mean().reset_index().min()
    avgMax = byDay.mean().reset_index().max()
    
    def day(day):
        date = datetime.fromtimestamp(day * (60 * 60 * 24))
        return date.strftime("%d.%m.%Y")
    
    print('Najmensie meskanie: ' + day(min['day']) + ' (' + minutes(min['delay']) + ')')
    print('Najvecsie meskanie: ' + day(max['day']) + ' (' + minutes(max['delay']) + ')')
    print('Najmensie priemerne meskanie: ' + day(avgMin['day']) + ' (' + minutes(avgMin['delay']) + ')')
    print('Najvecsie priemerne meskanie: ' + day(avgMax['day']) + ' (' + minutes(avgMax['delay']) + ')')

def stats(path, options):
    output = loadItems(path, options)

    itemsCount = len(output.items)
    if itemsCount > 0:
        print("Found " + str(itemsCount) + " entries")
        print("")
        #display statistics
        printStats(output)

        #display graph
        import plotStyle
        
        i = 0
        for someItems in output.stats.values():
            clr = plotStyle.tableau20[i % len(plotStyle.tableau20)]
            plt.plot(someItems, '-', color=clr)
            i += 1
        
        plotStyle.subplotStyle(plt.subplot(111))
        plotStyle.style(plt)
        
        if options.show:
            plt.show()
        else:
            plt.savefig("out.png", bbox_inches="tight")  
    else:
        print("No entries were found")