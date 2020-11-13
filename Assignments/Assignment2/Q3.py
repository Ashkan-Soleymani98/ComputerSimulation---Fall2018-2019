import numpy as np
import pandas as pd
import random
import openpyxl
import math


def simulate(fileName, interArrivals, serviceTimes, customersSize):
    customerWaits = list()
    customersWorkTimes = list()
    arrivalTimes = [0]

    for i in interArrivals:
        arrivalTimes.append(arrivalTimes[-1] + i)

    # print(*interArrivals)
    # print(*serviceTimes)
    # print(*arrivalTimes)

    customersList = [i for i in range(customersSize)]

    # print(*customersList)
    simulationTableString = list()
    simulationTableTitles = ['time', 'bi(t)', 'LQ(t)', 'Future Event List', 'Total Busy Time', 'Total Wait Time',
                             'Ns', 'System Wait']
    simulationTable = dict((i, list()) for i in simulationTableTitles)

    busyTime = 0
    systemWaitTime = 0
    waitTime = 0
    Ns = 0
    time = 0
    queue = list()
    idle = True
    stepTime = 1
    while queue or customersList or not idle:
        if not idle:
            busyTime += stepTime
            waitTime += len(queue) if queue else 1
        if customersList:
            customer = customersList[0]
            while arrivalTimes[customer] <= time and customersList:
                customer = customersList[0]
                queue.append(customersList.pop(0))
        if queue and idle:
            beingServicedCustomer = queue.pop(0)
            startingServiceTime = time
            idle = False
            bi = False
        if not idle:
            if time >= startingServiceTime + serviceTimes[beingServicedCustomer]:
                idle = True
                bi = True if len(queue) == 0 else False
                customerWaits.append(startingServiceTime - arrivalTimes[beingServicedCustomer])
                customersWorkTimes.append(time - startingServiceTime)
                Ns += 1

        if bi:
            systemWaitTime += 1

        simulationTableString.append("time= " + str(time) + ", bi(t)= " + str(bi) + ", LQ(t)= " + str(max(len(queue) - 1, 0)) \
                                     + ", busy time= " + str(busyTime) + ", wait time= " + str(waitTime)
                                     + ",Ns= " + str(Ns) + ",system wait time= " + str(systemWaitTime))
        simulationTable['time'].append(time)
        simulationTable['bi(t)'].append(bi)
        simulationTable['LQ(t)'].append(max(len(queue) - 1, 0))
        nextArrival = ('A', arrivalTimes[customersList[0]] if customersList else float('inf'))
        nextDeparture = ('D', serviceTimes[beingServicedCustomer] + startingServiceTime if not idle
        else (time + serviceTimes[queue[0]] if queue else float('inf')))
        FEL = sorted([tuple(reversed(nextArrival)), tuple(reversed(nextDeparture))])
        FEL = [tuple(reversed(i)) for i in FEL]
        FEL = [i[:-1] + (('-',) if i[-1] == float('inf') else (i[-1],)) for i in FEL]
        simulationTable['Future Event List'].append(FEL)
        simulationTable['Total Busy Time'].append(busyTime)
        simulationTable['Total Wait Time'].append(waitTime)
        simulationTable['System Wait'].append(systemWaitTime)
        simulationTable['Ns'].append(Ns)
        time += stepTime

    print("Customer Wait Mean= " + str(sum(customerWaits) / customersSize))
    # print(sum(serviceTimes) == sum(customersWorkTimes))
    # print(sum(serviceTimes), sum(customersWorkTimes))
    print("Customer Work Time Mean= " + str(sum(serviceTimes) / customersSize))
    # for i in simulationTableString:
    #     print(i)
    mainTable = pd.DataFrame({'time': simulationTable['time'],
                              'bi(t)': simulationTable['bi(t)'],
                              'LQ(t)': simulationTable['LQ(t)'],
                              'Future Event List': simulationTable['Future Event List'],
                              'System Wait': simulationTable['System Wait'],
                              'Total Busy Time': simulationTable['Total Busy Time'],
                              'Total Wait Time': simulationTable['Total Wait Time'],
                              'Ns': simulationTable['Ns']
                              })

    # print(dataframe)

    writer = pd.ExcelWriter(fileName + '.xlsx')
    mainTable.to_excel(writer, 'Sheet1')
    writer.save()

    return mainTable, simulationTable, time


def CDFReverseExp(lambd, n):
    Exps = []
    for i in range(n):
        r = random.uniform(0, 1)
        Exps.append(math.floor((-1) * np.log(1 - r) / lambd))
    return Exps


numOfCustomers = 100

lambda1 = 1 / 90
lambda2 = 1 / 75

interArrivals = CDFReverseExp(lambda1, numOfCustomers)
serviceTimes = CDFReverseExp(lambda2, numOfCustomers)

fileName = 'Simulation Table'

simulationTable, mainTable, elapsedTime = simulate(fileName, interArrivals, serviceTimes, numOfCustomers)

print("Mean Queue Length = " + str(simulationTable['LQ(t)'].sum() / elapsedTime))
print("Simulation Table is Saved in an Excel File Named " + fileName)
print()
print(simulationTable)
# print("Mean Wait = " + str(simulationTable['Total Wait Time'][-1] / numOfCustomers))

# print(simulationTable)





