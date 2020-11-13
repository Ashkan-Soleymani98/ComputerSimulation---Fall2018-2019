import math
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = (12, 8)


# Question1-part1
print("Please Enter the Number of Wanted LCMs to Set Up CLCG: k")
k = int(input())

print("Please Enter the Variables of LCMs Consequently: a, c, m, X0")
As = []
Cs = []
Ms = []
Xis = [[] for i in range(k)]
for i in range(k):
    print("Please Enter: a" + str(i + 1) + ", c" + str(i + 1) + ", m" + str(i + 1) + ", X0." + str(i + 1))
    inp = list(map(int, input().split()))
    As.append(inp[0])
    Cs.append(inp[1])
    Ms.append(inp[2])
    Xis[i].append(inp[3])

# print(As)
# print(Cs)
# print(Ms)
# print(Xis)

hang = Ms[0] - 1

print("Please Enter the Length of Wanted Random Sequence")
n = int(input())

Xs = []
for i in range(n):
    randomVar = 0
    coeff = 1
    for j, X in enumerate(Xis):
        X.append((As[j] * X[-1] + Cs[j]) % Ms[j])
        randomVar += coeff * X[-1] % hang
        coeff *= -1
    randomVar = randomVar % hang
    if randomVar == 0:
        randomVar = hang
    Xs.append(randomVar)

Rs = []
for i in Xs:
    Rs.append(i / Ms[0])

print("Uniformly Distributed Random Variables between 0, 1:")
print(Rs)

plt.hist(Rs, density=True)
plt.show()

# Question1-part2


def CDFReverseExp(Rs):
    Exps = []
    lambd = 2
    for r in Rs:
        Exps.append((-1) * np.log(1 - r) / lambd)
    return Exps


Exps = CDFReverseExp(Rs)
print("Exponentially Distributed Random Variables with Parameter lambda = 2:")
print(Exps)

plt.hist(Exps, density=True)
plt.show()


def CDFReverseTriang(Rs):
    Triangs = []
    for r in Rs:
        if 0 <= r <= 0.5:
            Triangs.append(math.sqrt(8 * r))
        else:
            Triangs.append(4 - math.sqrt(8 * (1 - r)))
    return Triangs


Triangs = CDFReverseTriang(Rs)
print("Triangularly Distributed Random Variables:")
print(Triangs)

plt.hist(Triangs, density=True)
plt.show()



