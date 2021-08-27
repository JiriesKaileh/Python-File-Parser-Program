import os                                #for accessing and iterating through directories
import statistics                        #for calculating standard deviation
import matplotlib.pyplot as plt          #for generating histogram
from statsmodels.graphics import tsaplots  #for autocorrelation function
import numpy as np                       #for autocorrelation
import scipy
from scipy import signal
from pandas import read_csv
from statsmodels.graphics.tsaplots import plot_acf

import csv

class Event():
    scope = ''             #initialized to null string
    timestamp = 0          #initialized to zero
    voltage = 0            #this is the voltage from the ramp. It is initialized to zero
    isMatched = False      #initialized to false because the event hasn't been matched to a corrsponding one yet

    def __init__(self, scp, time, volt):  #we will include voltage as soon as we figure out how to record from multiple sources in Waveforms 2015
        self.scope = scp
        self.timestamp = time
        self.voltage = volt


#anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\\anode'  #folder path to .csv acquisitions for AD1 in scenario 1
#pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\pmt'      #folder path to .csv acquisitions for AD2 in scenario 1

#anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD1 run 27'   #folder path to .csv acquisitions for AD1 in scenario 1
#pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD2 run 27'      #folder path to .csv acquisitions for AD2 in scenario 1

anodeDir = 'C:\\Users\\skyfab\Documents\\Waveforms\\Data Scenario 1 with voltages\\AD1'   #folder path to .csv acquisitions for AD1 in scenario 1
pmtDir = 'C:\\Users\\skyfab\Documents\\Waveforms\\Data Scenario 1 with voltages\\AD2'      #folder path to .csv acquisitions for AD2 in scenario 1


anode = []

pmt = []

difsXaxis = []                                                     #number of time differences recorded





for filename in os.listdir(anodeDir):
    name = os.path.join(anodeDir, filename)                        #store the name of the file in 'name'
    index = len(name) - 5                                          #len(name) is the number of characters in name, and len(name) - 5 is ones place of the milliseconds in the timestamp 
                                                                   #example: name = 'C:\Users\skyfab\Documents\Waveforms\Data\anode\anode12.25.43.116.csv' 
                                                                   #the character name[index] corresponds to 6. We use the function int() to cast the character to an integer value
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds

    #anodeTimes.append(timeStampVal)                                 #add timestamp value to anodeTimes
    
    volt = 0
    
    with open(name) as f:
        rows = list(csv.reader(f))
        volt += float(rows[21][1])
    

    anode.append(Event("AD1", timeStampVal, volt))

  

for filename in os.listdir(pmtDir):
    name = os.path.join(pmtDir, filename)                          
    index = len(name) - 5
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds


    #pmtTimes.append(timeStampVal)                                   #add timestamp value to pmtTimes

    volt = 0
    
    with open(name) as f:
        rows = list(csv.reader(f))
        volt += float(rows[21][1])
        

    pmt.append(Event("AD2", timeStampVal, volt))

#the following section is supposed to get rid of acquisition duplicates

'''
Evan's within dT = 10 milliseconds algorithm

step 1: determine which oscilloscope took more acquisitions. This is the list we are going to pop aquisitions from

step 2: start at the beginning of the larger list and see if the acquisition across is within 10 seconds.
        if it is, move on to the next acquisition in the larger list.
        If not, check if the next acquisition has a smaller time difference
            if it is, check if the acquisition is within 10 seconds. if not check if the next acquisition has a smaller time difference

            if not, move on to the next acquisition in the larger list 
'''

pairedAnode = []              #these lists will contain the paired acquisitions

pairedPmt = []


numTossed = 0                  #number of events removed

anodeLen = len(anode)          #
pmtLen = len(pmt)


#for when pmt has more acquisitions than anode 
if(pmtLen > anodeLen):
        for i in range(len(anode)):
            wasMatch = False

            if(i == 0):             #if you are looking at the first element in the large list, compare it to the next three acquisitions
                for j in range(3):
                    if(abs(anode[i].timestamp - pmt[i + j].timestamp) < 10 and not anode[i].isMatched and not pmt[i+j].isMatched):
                        pairedAnode.append(anode[i])
                        pairedPmt.append(pmt[i + j])
                        anode[i].isMatched = True
                        pmt[i + j].isMatched = True
                        wasMatch = True
            elif(i == len(anode) - 1): #if you are looking at the last element in the large list, compare it to the next three acquisitions
                for j in range(3):
                    if(abs(anode[i].timestamp - pmt[i - j].timestamp) < 10 and not anode[i].isMatched and not pmt[i-j].isMatched):
                        pairedAnode.append(anode[i])
                        pairedPmt.append(pmt[i - j])
                        anode[i].isMatched = True
                        pmt[i - j].isMatched = True
                        wasMatch = True
            else:
                for j in range(3):
                    if(abs(anode[i].timestamp - pmt[i - 1 + j].timestamp) < 10 and not anode[i].isMatched and not pmt[i - 1 + j].isMatched):
                            pairedAnode.append(anode[i])
                            pairedPmt.append(pmt[i - 1 + j])
                            anode[i].isMatched = True
                            pmt[i - 1 + j].isMatched = True 
                            wasMatch = True

            if(not wasMatch):
                numTossed += 1


#for when anode has more acquisitions than pmt
if(anodeLen > pmtLen):
    for i in range(len(pmt)):
        wasMatch = False

        if(i == 0):             #if you are looking at the first element in the large list, compare it to the next three acquisitions
            for j in range(3):
                if(abs(pmt[i].timestamp - anode[i + j].timestamp) < 10 and not pmt[i].isMatched and not anode[i+j].isMatched):
                    pairedPmt.append(pmt[i])
                    pairedAnode.append(anode[i + j])
                    pmt[i].isMatched = True
                    anode[i + j].isMatched = True
                    wasMatch = True
        elif(i == len(pmt) - 1): #if you are looking at the last element in the large list, compare it to the next three acquisitions
            for j in range(3):
                if(abs(pmt[i].timestamp - anode[i - j].timestamp) < 10 and not pmt[i].isMatched and not anode[i-j].isMatched):
                    pairedPmt.append(pmt[i])
                    pairedAnode.append(anode[i - j])
                    pmt[i].isMatched = True
                    anode[i - j].isMatched = True
                    wasMatch = True
        else:
            for j in range(3):
                if(abs(pmt[i].timestamp - anode[i - 1 + j].timestamp) < 10 and not pmt[i].isMatched and not anode[i - 1 + j].isMatched):
                        pairedPmt.append(pmt[i])
                        pairedAnode.append(anode[i - 1 + j])
                        pmt[i].isMatched = True
                        anode[i - 1 + j].isMatched = True 
                        wasMatch = True
        
        if(not wasMatch):
            numTossed += 1

'''
if(anodeLen > pmtLen):
    for i in range(len(anode):
        isMatched = False
        for j in range(3):
            if(abs(anode[i].timestamp - pmt[i +j].timestamp) < 10 and not isMatched):
                pairedAnode.append(anode[i])
                pairedPmt.append(pmt[i + j])
                isMatched = True
elif(pmtLen > anodeLen):
    for i in range(len(pmt)):
        isMatched = False
        for j in range(3):
            if(abs(pmt[i].timestamp - anode[i+ j].timestamp) < 10 and not isMatched):
                pairedPmt.append(pmt[i])
                pairedAnode.append(anode[i+j])
                isMatched = True                
'''       

    
    



#The following section can be uncommented to display the timestamp values in anodeTimes and pmtTimes
#This process slows down the program

'''
print("-------------------- now displaying anodeTimes --------------") 

for i in range(len(anodeTimes)):                                        #iterate through and print timestamp values of anodeTimes
    print(anodeTimes[i])
    print('\n')

print("-------------------- now displaying pmtTimes --------------")
 
for i in range(len(pmtTimes)):                                          #iterate through and print timestamp values of pmtTimes
    print(pmtTimes[i])
    print('\n')
'''





timeDifs = [] #difference between timestamps is stored here
voltDifs = [] #difference between voltages is stored here


count = 1  #serves as an index for the time differences

#for a, p in zip(anodeTimes, pmtTimes): 
for a, p in zip(pairedAnode, pairedPmt):
    #timeDifs.append( abs(a - p) )
    timeDifs.append(abs(a.timestamp - p.timestamp))
    voltDifs.append(abs(a.voltage - p.voltage))
    print("%1d %10d %20s %10f %20s %f %20s %10d" % (count, abs(a.timestamp - p.timestamp), "anode voltage: ", a.voltage, "pmt voltage: ", p.voltage, "voltage diff: ", abs(a.voltage - p.voltage)))
    difsXaxis.append(count)
    count += 1

print("\n")








print("The average time difference between the two oscilloscopes is: ")
print(sum(timeDifs) / len(timeDifs))                                        #print average
print("\n")
print("the standard deviation is:")                                         #print standard deviation
print(statistics.stdev(timeDifs))
print("\n")
print("the median is:")
print(statistics.median(timeDifs))                                                     #print median

print('\n\n')

print("The average voltage difference between the two oscilloscopes is: ")               #not sure if I want to plot this yet
print(sum(voltDifs) / len(voltDifs))                                        #print average
print("\n")
print("the standard deviation is:")                                         #print standard deviation
print(statistics.stdev(voltDifs))
print("\n")
print("the median is:")
print(statistics.median(voltDifs))      

print('\n\n')

print("the number of acquisitions for AD1 is:")                                         #print number of acquisitions
print(len(pairedAnode))
print("the number of acquisitions for AD2 is:")
print(len(pairedPmt))

print('\n\n')

print("The number of acquisitions tossed is:")
print(numTossed)

#figure something out for bipolar distributions

#The following lines generate a histogram in a popup window


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)   # create figure and axes

ax1.hist(timeDifs, bins = 'auto')                                #figure out how to make bin width 1 ms
ax1.set_title('Time Differences')
ax1.set_xlabel('Time Difference in Milliseconds')
ax1.set_ylabel('Frequency')


count = 1


anodeXaxis = []
pmtXaxis = []


while(count <= len(pairedAnode)):
    anodeXaxis.append(count)
    count += 1

count = 1

#while(count <= len(pmtTimes)):
while(count <= len(pairedPmt)):
    pmtXaxis.append(count)
    count += 1


#ax2.scatter(anodeXaxis, anodeTimes, color="b")
#ax2.scatter(pmtXaxis, pmtTimes, color="r", marker="P")

anodeTimes = []

pmtTimes = []

for i in range(len(pairedAnode)):
    anodeTimes.append(pairedAnode[i].timestamp)

for i in range(len(pairedPmt)):
    pmtTimes.append(pairedPmt[i].timestamp)


ax2.scatter(anodeXaxis, anodeTimes, color="b")
ax2.scatter(pmtXaxis, pmtTimes, color="r", marker="P")

ax2.set_xlabel('acquisition number')
ax2.set_ylabel('Time in miliseconds')         

ax3.scatter(difsXaxis, timeDifs)

ax3.set_xlabel('acq number')
ax3.set_ylabel('Time difs in miliseconds') 


#corr = signal.correlate(anodeTimes, pmtTimes, mode = 'full', method = 'auto')
corr = signal.correlate(anodeTimes, pmtTimes, mode = 'full', method = 'auto')


ax4.plot(corr)

'''
autocorr = np.correlate(anodeTimes, pmtTimes, mode = 'valid')

print('\n\n')

for i in range(len(autocorr)):
    print(autocorr[i])
'''

plt.show()




#pmt folder usually has one more acquisition than the anode folder. This can cause l#arge discrepancies when 
#multiple acquisitions runs are kept in the same folder as non-corresponding acquisitions are subtracted
#resulting in huge differences. 

