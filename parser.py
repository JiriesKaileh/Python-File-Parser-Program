import os                                #for accessing and iterating through directories
import statistics                        #for calculating standard deviation
import matplotlib.pyplot as plt          #for generating histogram
#import numpy as np                       #for generating histogram


#anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\\anode'  #folder path to .csv acquisitions for AD1 in scenario 1
#pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 2\pmt'      #folder path to .csv acquisitions for AD2 in scenario 1

anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\\AD1'   #folder path to .csv acquisitions for AD1 in scenario 1
pmtDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1\AD2'      #folder path to .csv acquisitions for AD2 in scenario 1


anodeTimes = []                                                    #list in which timestamps for anodeTimes is stored
pmtTimes = []                                                      #list in which timestamps for pmtTimes is stored
xAxis = []





for filename in os.listdir(anodeDir):
    name = os.path.join(anodeDir, filename)                        #store the name of the file in 'name'
    index = len(name) - 5                                          #len(name) is the number of characters in name, and len(name) - 5 is ones place of the milliseconds in the timestamp 
                                                                   #example: name = 'C:\Users\skyfab\Documents\Waveforms\Data\anode\anode12.25.43.116.csv' 
                                                                   #the character name[index] corresponds to 6. We use the function int() to cast the character to an integer value
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds

    anodeTimes.append(timeStampVal)                                 #add timestamp value to anodeTimes
  

for filename in os.listdir(pmtDir):
    name = os.path.join(pmtDir, filename)                          
    index = len(name) - 5
  
    timeStampVal = int(name[index - 8]) * 600000 + int(name[index - 7]) * 60000 + int(name[index - 5]) * 10000 + int(name[index - 4]) * 1000 + int(name[index - 2]) * 100 + int(name[index - 1]) * 10 + int(name[index]) #converting the timestamp to milliseconds


    pmtTimes.append(timeStampVal)                                   #add timestamp value to pmtTimes






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

for a, p in zip(anodeTimes, pmtTimes): 
    timeDifs.append( abs(a - p) )
    print(count, abs( a - p ))        #This can be uncommented to print the index then the time difference, however this slows down the program
    xAxis.append(count)
    count = count + 1

print("\n")






print("The average time difference between the two oscilloscopes is: ")
print(sum(timeDifs) / len(timeDifs))                                        #print average
print("\n")
print("the standard deviation is:")                                         #print standard deviation
print(statistics.stdev(timeDifs))
print("\n")
print("the median is:")
print(statistics.median(timeDifs))                                                     #print median

#figure something out for bipolar distributions

#The following lines generate a histogram in a popup window

nCols = 1

nRows = 1

fig, (ax1, ax2) = plt.subplots(2)   # create figure and axes

ax1.hist(timeDifs, bins = 'auto')
ax1.set_title('Time Differences')
ax1.set_xlabel('Time Difference in Milliseconds')
ax1.set_ylabel('Frequency')
ax2.scatter(xAxis, anodeTimes)
#ax2.scatter(xAxis, pmtTimes)
ax2.set_title('Time versus acq number')
ax2.set_xlabel('acq number')
ax2.set_ylabel('Time in Milliseconds')
plt.show()
#plt.show()
#plt.scatter(anodeTimes, xAxis)
#plt.scatter(pmtTimes, xAxis)




#pmt folder usually has one more acquisition than the anode folder. This can cause large discrepancies when 
#multiple acquisitions runs are kept in the same folder as non-corresponding acquisitions are subtracted
#resulting in huge differences. 

