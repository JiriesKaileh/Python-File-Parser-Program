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
    scope = ''            #initialized to null string
    timestamp = 0          #initialized to zero
    voltage = 0            #this is the voltage from the ramp. It is initialized to zero

    def __init__(self, scp, time):  #we will include voltage as soon as we figure out how to record from multiple sources in Waveforms 2015
        self.scope = scp
        self.timestamp = time


#anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\\anode'  #folder path to .csv acquisitions for AD1 in scenario 1
#pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\pmt'      #folder path to .csv acquisitions for AD2 in scenario 1

anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD1 run 24'   #folder path to .csv acquisitions for AD1 in scenario 1
pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD2 run 24'      #folder path to .csv acquisitions for AD2 in scenario 1


#anodeTimes = []                                                    #list in which timestamps for anodeTimes is stored
anode = []

#pmtTimes = []                                                      #list in which timestamps for pmtTimes is stored
pmt = []

difsXaxis = []                                                     #number of time differences recorded





for filename in os.listdir(anodeDir):
    name = os.path.join(anodeDir, filename)                        #store the name of the file in 'name'
    index = len(name) - 5                                          #len(name) is the number of characters in name, and len(name) - 5 is ones place of the milliseconds in the timestamp 
                                                                   #example: name = 'C:\Users\skyfab\Documents\Waveforms\Data\anode\anode12.25.43.116.csv' 
                                                                   #the character name[index] corresponds to 6. We use the function int() to cast the character to an integer value
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds

    #anodeTimes.append(timeStampVal)                                 #add timestamp value to anodeTimes

    anode.append(Event("AD1", timeStampVal))
  

for filename in os.listdir(pmtDir):
    name = os.path.join(pmtDir, filename)                          
    index = len(name) - 5
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds


    #pmtTimes.append(timeStampVal)                                   #add timestamp value to pmtTimes

    pmt.append(Event("AD2", timeStampVal))

#the following section is supposed to get rid of acquisition duplicates

'''
description for aligning nearest timestamps

step 1: determine which oscilloscope took more acquisitions. This is the list we are going to pop acquisitions from

step 2: start at the beginning of the smaller list and compare across and 1 up
        if the smaller list acquisition is closer to the larger list acquisition that is across, then do nothing
        if the smaller list acquisition is closer to the next larger list acquisition, then pop the acquisition in the larger list

iterate through the list. Using this algorithm, we may or may not end up with the same number of acquisitions.
we may need to compare the current acquisition to more than just the next one

'''

choice = input("Would you like to run the acquisition alignment algorithm? (Y/N): ")

if(choice.upper() == 'Y'):
    for i in range(max(len(anode), len(pmt))):
        if(len(anode) > len(pmt)):
            if(abs(anode[i+1].timestamp - pmt[i].timestamp) < abs(anode[i].timestamp - pmt[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                    print("removing acquisition number:", i, "with a timestamp of:", anode[i].timestamp, "\n")
                    anode.pop(i)
        elif(len(pmt) > len(anode)):
            if(abs(pmt[i+1].timestamp - anode[i].timestamp) < abs(pmt[i].timestamp - anode[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                print("removing acquisition number:", i, "with a timestamp of:", pmt[i].timestamp, "\n")
                pmt.pop(i)
'''
length = len(anode) - 1

i = 0

while( i < length):
	if(anode[i + 1].timestamp < anode[i].timestamp + 30):
		anode.pop( i+1 )
		length -= 1
	i += 1

length = len(pmt) - 1

i = 0

while( i < length):
	if(pmt[i + 1].timestamp < pmt[i].timestamp + 30):
		pmt.pop( i+1 )
		length -= 1
	i += 1
'''


'''
if(len(anode) > len(pmt)):
        for i in range(len(pmt) - 1):
            if(abs(anode[i+1].timestamp - pmt[i].timestamp) < abs(anode[i].timestamp - pmt[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                anode.pop(i)
    elif(len(pmt) > len(anode)):
        for i in range(len(anode) - 1):
            if(abs(pmt[i+1].timestamp - anode[i].timestamp) < abs(pmt[i].timestamp - anode[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                pmt.pop(i)
'''


#keep track of the list with the smallest list to prevent index errors. In some cases you remove enough acquisitions such that the larger list became smaller than the smaller list

#if the acquisitions are equal, then do nothing.


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


count = 1  #serves as an index for the time differences

#for a, p in zip(anodeTimes, pmtTimes): 
for a, p in zip(anode, pmt):
    #timeDifs.append( abs(a - p) )
    timeDifs.append(abs(a.timestamp - p.timestamp))
    print(count, abs( a.timestamp - p.timestamp ))        #This can be uncommented to print the index then the time difference, however this slows down the program
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

print("the number of acquisitions for AD1 is:")                                         #print number of acquisitions
print(len(anode))
print("the number of acquisitions for AD2 is:")
print(len(pmt))

#figure something out for bipolar distributions

#The following lines generate a histogram in a popup window


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)   # create figure and axes

ax1.hist(timeDifs, bins = 'auto')
ax1.set_title('Time Differences')
ax1.set_xlabel('Time Difference in Milliseconds')
ax1.set_ylabel('Frequency')


count = 1


anodeXaxis = []
pmtXaxis = []


#while(count <= len(anodeTimes)):
while(count <= len(anode)):
    anodeXaxis.append(count)
    count += 1

count = 1

#while(count <= len(pmtTimes)):
while(count <= len(pmt)):
    pmtXaxis.append(count)
    count += 1


#ax2.scatter(anodeXaxis, anodeTimes, color="b")
#ax2.scatter(pmtXaxis, pmtTimes, color="r", marker="P")

anodeTimes = []

pmtTimes = []

for i in range(len(anode)):
    anodeTimes.append(anode[i].timestamp)

for i in range(len(pmt)):
    pmtTimes.append(pmt[i].timestamp)


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

