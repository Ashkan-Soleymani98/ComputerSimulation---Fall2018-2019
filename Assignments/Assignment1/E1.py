import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


customersSize = 200


def simulate(fileName, interArrivalsDistr, serviceTimeDistr):
    print(fileName)
    interArrivals = list()
    serviceTimes = list()
    for i, j in interArrivalsDistr:
        count = int(j * customersSize)
        interArrivals.extend([i for k in range(count)])

    for i, j in serviceTimesDistr:
        count = int(j * customersSize)
        serviceTimes.extend([i for k in range(count)])


    interArrivals = np.random.permutation(interArrivals)
    serviceTimes = np.random.permutation(serviceTimes)
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
            while arrivalTimes[customer] <= time:
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

    return simulationTable


simulationTables = list()


# Probability Distributions
interArrivalsDistr = [(1, 0.2), (2, 0.2), (3, 0.2), (4, 0.2), (5, 0.2)]
serviceTimesDistr = [(2, 0.28), (3, 0.19), (5, 0.23), (6, 0.18), (9, 0.12)]

simulationTables.append((simulate('Question Data', interArrivalsDistr, serviceTimesDistr), 'Question Data'))


# Probability Distributions in Modified State
interArrivalsDistr = [(2, 0.2), (3, 0.2), (4, 0.2), (5, 0.2), (6, 0.2)]
serviceTimesDistr = [(2, 0.28), (3, 0.19), (5, 0.23), (6, 0.18), (9, 0.12)]


simulationTables.append((simulate('Modified Data1', interArrivalsDistr,  serviceTimesDistr), 'Modified Data1'))


interArrivalsDistr = [(3, 0.2), (4, 0.2), (5, 0.2), (6, 0.2), (7, 0.2)]
serviceTimesDistr = [(2, 0.28), (3, 0.19), (5, 0.23), (6, 0.18), (9, 0.12)]


simulationTables.append((simulate('Modified Data2', interArrivalsDistr,  serviceTimesDistr), 'Modified Data2'))


interArrivalsDistr = [(4, 0.2), (5, 0.2), (6, 0.2), (7, 0.2), (8, 0.2)]
serviceTimesDistr = [(2, 0.28), (3, 0.19), (5, 0.23), (6, 0.18), (9, 0.12)]


simulationTables.append((simulate('Modified Data3', interArrivalsDistr,  serviceTimesDistr), 'Modified Data3'))


for i in simulationTables:
    plt.plot(i[0]['time'], i[0]['LQ(t)'], label=i[1])
plt.ylabel('LQ(t)')
plt.xlabel('time')

leg = plt.legend(loc='best', ncol=1, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)

plt.show()


for i in simulationTables:
    plt.plot(i[0]['Total Busy Time'], i[0]['System Wait'], label=i[1])
plt.xlabel('Total Busy Time')
plt.ylabel('System Wait')

leg = plt.legend(loc='best', ncol=1, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)

plt.show()

for i in simulationTables:
    plt.plot(i[0]['time'], i[0]['Ns'], label=i[1])
plt.ylabel('Ns')
plt.xlabel('time')

leg = plt.legend(loc='best', ncol=1, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.5)


plt.show()

