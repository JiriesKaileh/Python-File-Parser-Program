import csv
import os


anodeDir = 'C:\\Users\\skyfab\\Documents\\Waveforms\\Data Scenario 1 with voltages test folder\\AD1'

anodeVoltages = []


for filename in os.listdir(anodeDir):
    name = os.path.join(anodeDir, filename)                      


    with open(name) as f:
        rows = list(csv.reader(f))
        anodeVoltages.append(rows[21][1])                      #prints the first voltage value recorded in channel 1
      


for i in range(len(anodeVoltages)):
    print(anodeVoltages[i])
    print('\n')

