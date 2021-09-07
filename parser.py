import os                                #for accessing and iterating through directories
import statistics                        #for calculating standard deviation
import matplotlib.pyplot as plt          #for generating histogram
from statsmodels.graphics import tsaplots  #for autocorrelation function
import numpy as np                       #for autocorrelation
import scipy
from scipy import signal
import scipy.stats as stats
from pandas import read_csv
from statsmodels.graphics.tsaplots import plot_acf

import csv

class Event():
    scope = ''             #The name of the oscilloscope the acquisition came from. Initialized to null string
    timestamp = 0          #The timestamp value in milliseconds. Initialized to zero
    voltage = 0            #This is the voltage from the ramp in volts. It is initialized to zero

    def __init__(self, scp, time, volt):  #we will include voltage as soon as we figure out how to record from multiple sources in Waveforms 2015
        self.scope = scp
        self.timestamp = time
        self.voltage = volt


#anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\\anode'  #folder path to .csv acquisitions for AD1 in scenario 1
#pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\pmt'      #folder path to .csv acquisitions for AD2 in scenario 1

anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD1 run 32'   #folder path to .csv acquisitions for AD1 in scenario 1
pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD2 run 32'      #folder path to .csv acquisitions for AD2 in scenario 1

#anodeDir = 'C:\\Users\\skyfab\Documents\\Waveforms\\Data Scenario 1 with voltages\\AD1 run 5'   #folder path to .csv acquisitions for AD1 in scenario 1 with voltage measurements
#pmtDir = 'C:\\Users\\skyfab\Documents\\Waveforms\\Data Scenario 1 with voltages\\AD2 run 5'      #folder path to .csv acquisitions for AD2 in scenario 1 with voltage measurements

anode = []

pmt = []

difsXaxis = []                                                     #number of time differences recorded



for filename in os.listdir(anodeDir):
    name = os.path.join(anodeDir, filename)                        #store the name of the file in 'name'
    index = len(name) - 5                                          #len(name) is the number of characters in name, and len(name) - 5 is ones place of the milliseconds in the timestamp 
                                                                   #example: name = 'C:\Users\skyfab\Documents\Waveforms\Data\anode\anode12.25.43.116.csv' 
                                                                   #the character name[index] corresponds to 6. We use the function int() to cast the character to an integer value
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds
    
    volt = 0
    
    with open(name) as f:                 #get first voltage measurement from csv file
        rows = list(csv.reader(f))
        volt += (float(rows[21][1]) * 1000)     #multiplying by 1000 to convert from V to mV
    

    anode.append(Event("AD1", timeStampVal, volt))    #Create event and add it to the list anode

  
#Same idea as previous loop but with pmt
for filename in os.listdir(pmtDir):
    name = os.path.join(pmtDir, filename)                        
    index = len(name) - 5                         
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) 

    volt = 0
    
    with open(name) as f:                
        rows = list(csv.reader(f))
        volt += (float(rows[21][1]) * 1000)       
        

    pmt.append(Event("AD2", timeStampVal, volt))          


#the following section pairs acquisitions
'''
Description of Acquisition Alignment Algorithm

step 1: determine which oscilloscope took more acquisitions. This is the list we are going to pop (remove) acquisitions from

step 2: start at the beginning of the smaller list and compare across and 1 up
        if the smaller list acquisition is closer to the larger list acquisition that is across, then do nothing
        if the smaller list acquisition is closer to the next larger list acquisition, then pop the current acquisition in the larger list

repeat throughout the list
'''

choice = input("Would you like to run the Acquisition Alignment Algorithm? (Y/N): ")




if(choice.upper() == 'Y'):
    choice2 = input("would you like to use the deprecated or updated version? (D/U): ")

    #Deprecated Aquisition Alignment Algorithm
    if(choice2.upper() == "D"):
        for i in range(max(len(anode), len(pmt))):
            if(len(anode) > len(pmt)):
                if(abs(anode[i+1].timestamp - pmt[i].timestamp) < abs(anode[i].timestamp - pmt[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                        print("removing acquisition number:", i, "with a timestamp of:", anode[i].timestamp, "\n")
                        anode.pop(i)
            elif(len(pmt) > len(anode)):
                if(abs(pmt[i+1].timestamp - anode[i].timestamp) < abs(pmt[i].timestamp - anode[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                    print("removing acquisition number:", i, "with a timestamp of:", pmt[i].timestamp, "\n")
                    pmt.pop(i)


    #Updated New Aquisition Alignment Algorithm
    elif(choice2.upper() == 'U'):
        i = 0

        while(i < max(len(anode), len(pmt))):
            if(len(anode) > len(pmt)):
                isDecreasing = True
                
                while(isDecreasing):   
                    if(abs(anode[i+1].timestamp - pmt[i].timestamp) < abs(anode[i].timestamp - pmt[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                        print("removing acquisition number:", i, "with a timestamp of:", anode[i].timestamp, "\n")
                        anode.pop(i)
                    else:
                        isDecreasing = False

            elif(len(pmt) > len(anode)):
                isDecreasing = True

                while(isDecreasing):
                    if(abs(pmt[i+1].timestamp - anode[i].timestamp) < abs(pmt[i].timestamp - anode[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                        print("removing acquisition number:", i, "with a timestamp of:", pmt[i].timestamp, "\n")
                        pmt.pop(i)
                    else:
                        isDecreasing = False
                        

            i += 1


'''
#first version of acquisition alignment algorithm

if(len(anode) > len(pmt)):
        for i in range(len(pmt) - 1):
            if(abs(anode[i+1].timestamp - pmt[i].timestamp) < abs(anode[i].timestamp - pmt[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                anode.pop(i)
    elif(len(pmt) > len(anode)):
        for i in range(len(anode) - 1):
            if(abs(pmt[i+1].timestamp - anode[i].timestamp) < abs(pmt[i].timestamp - anode[i].timestamp) ): #if the next acquisition of the larger list is closer to the current acquisition of the smaller list, remove the current acquisition of the larger list
                pmt.pop(i)
'''

'''
#First "duplicate" eliminating algorithm. 
#doesn't work well.

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
voltTimeDifs = [] #the time difference produced from the slope of the ramp (50 mV/ms)


count = 1  #serves as an index for the time differences
'''
#old voltage difference method

for a, p in zip(anode, pmt):
    timeDifs.append(abs(a.timestamp - p.timestamp))           #add the difference of the corresponding acquistion timestamps to the timeDifs list
    voltDifs.append(abs(a.voltage - p.voltage))               #add the difference of the corresponding acquisition voltages to the voltDifs list
    voltTimeDifs.append(abs(a.voltage - p.voltage) / 50)      #dividing the voltage difference by the slope of the ramp to get the time difference
    print("%1d %10d %20s %10f %20s %f %20s %10f %20s %10f" % (count, abs(a.timestamp - p.timestamp), "anode voltage (mV): ", a.voltage, "pmt voltage (mV): ", p.voltage, "voltage diff (mV): ", abs(a.voltage - p.voltage), "truth time difference: ", abs(a.voltage - p.voltage) / 50))   #formatting of output
    difsXaxis.append(count)          #difsXaxis is the number of time differences in the timeDifs list. It will be used as the x-axis in the plot
    count += 1                       

print("\n")

#we have to figure out how to calculate time differences when the ramp drops because 
#the voltage difference becomes very large, but the time difference is calculated
#as much larger than it actually is.
'''


'''
for a, p in zip(anode, pmt):
    timeDifs.append(abs(a.timestamp - p.timestamp))           #add the difference of the corresponding acquistion timestamps to the timeDifs list
    
    #if you are subtracting a negative value and a positive value, shift the negative value up by 10 V
    if( (a.voltage < 0 and p.voltage < 0) or (a.voltage > 0 and p.voltage > 0)):    
        voltDifs.append(abs(a.voltage - p.voltage))                            #add the difference of the corresponding acquisition voltages to the voltDifs list 
        voltTimeDifs.append(abs(a.voltage - p.voltage) / 50)      #dividing the voltage difference by the slope of the ramp to get the time difference
    else:
        if(a.voltage < 0):
            voltDifs.append(abs((a.voltage + 10.15) - p.voltage) ) 
            voltTimeDifs.append(abs( (a.voltage + 10.15) - p.voltage) / 50)  #shift up by 10 V
        else:
             voltDifs.append(abs( a.voltage  - (p.voltage + 10.15) ))
             voltTimeDifs.append(abs( a.voltage - (p.voltage + 10.15) ) / 50) #shift up by 10 V      #you could rewrite as .append(voltDifs[count-1])

    print("%1d %10d %20s %10f %20s %f %20s %10f %20s %10f" % (count, abs(a.timestamp - p.timestamp), "anode voltage (mV): ", a.voltage, "pmt voltage (mV): ", p.voltage, "voltage diff (mV): ", voltDifs[count-1], "truth time difference: ",voltTimeDifs[count-1] ) )  #formatting of output
    difsXaxis.append(count)          #difsXaxis is the number of time differences in the timeDifs list. It will be used as the x-axis in the plot
    count += 1                       

print("\n")

'''

#'''
for a, p in zip(anode, pmt):
    timeDifs.append(abs(a.timestamp - p.timestamp))           #add the difference of the corresponding acquistion timestamps to the timeDifs list
    
    #if you are subtracting a negative value and a positive value, shift the negative value up by 10 V
    if( (a.voltage < 0 and p.voltage < 0) or (a.voltage > 0 and p.voltage > 0)):    
        voltDifs.append(abs(a.voltage - p.voltage))                            #add the difference of the corresponding acquisition voltages to the voltDifs list 
        voltTimeDifs.append(abs(a.voltage - p.voltage) / 50)      #dividing the voltage difference by the slope of the ramp to get the time difference
    else:
        if(a.voltage < 0):
            voltDifs.append(abs((a.voltage + 10.15) - p.voltage) ) 
            voltTimeDifs.append(abs( (a.voltage + 10.15) - p.voltage) / 50)  #shift up by 10 V
        else:
             voltDifs.append(abs( a.voltage  - (p.voltage + 10.15) ))
             voltTimeDifs.append(abs( a.voltage - (p.voltage + 10.15) ) / 50) #shift up by 10 V      #you could rewrite as .append(voltDifs[count-1])

    print("%1d %10d %20s %10f %20s %f %20s %10f %20s %10f" % (count, abs(a.timestamp - p.timestamp), "anode voltage (mV): ", a.voltage, "pmt voltage (mV): ", p.voltage, "voltage diff (mV): ", voltDifs[count-1], "truth time difference: ",voltTimeDifs[count-1] ) )  #formatting of output
    difsXaxis.append(count)          #difsXaxis is the number of time differences in the timeDifs list. It will be used as the x-axis in the plot
    count += 1                       

print("\n")

#'''


print("The average time difference between the two oscilloscopes is: ")
print(sum(timeDifs) / len(timeDifs))                                        #print average
print("\n")
print("the standard deviation is:")                                         #print standard deviation
print(statistics.stdev(timeDifs))
print("\n")
print("the median is:")
print(statistics.median(timeDifs))                                                     #print median

print('\n\n')

print("The average voltage difference between the two oscilloscopes is: ")               
print(sum(voltDifs) / len(voltDifs))                                        #print average
print("\n")
print("the standard deviation is:")                                         #print standard deviation
print(statistics.stdev(voltDifs))
print("\n")
print("the median is:")
print(statistics.median(voltDifs))                                                     #print median

print('\n\n')

print("the number of acquisitions for AD1 is:")                                         #print number of acquisitions
print(len(anode))
print("the number of acquisitions for AD2 is:")
print(len(pmt))



#The following lines generate a histogram in a popup window


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)                      # create figure and axes

ax1.hist(timeDifs, bins = 'auto')                                #figure out how to make bin width 1 ms
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

anodeTimes = []                         #holds anode timestamps

pmtTimes = []                           #holds pmt timestamps

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



corr = signal.correlate(anodeTimes, pmtTimes, mode = 'full', method = 'auto')


ax4.plot(corr)


#goodness plot
#expected data (voltTimeDifs)
#observed data (timeDifs)

fig2, (ax5, ax6) = plt.subplots(2) 

#stats.chisquare(f_obs = timeDifs, f_exp = voltTimeDifs)                    #chisquare(observedData, expectedData) 

ax5.scatter(difsXaxis, timeDifs, color = "b")
ax5.scatter(difsXaxis, voltTimeDifs, color = "r", marker = "P")

ax5.set_title('timeDifs and voltTimeDifs vs Acquisition Number')
ax5.set_xlabel('Acquisition Number')
ax5.set_ylabel('Time in milliseconds')

ax6.scatter(voltTimeDifs, timeDifs)
ax6.set_xlabel('voltage time difference')
ax6.set_ylabel('timestamp time difference')

plt.show()