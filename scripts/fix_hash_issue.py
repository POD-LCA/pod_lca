from pod_lca.units import METER
from pod_lca.units import Quantity as Q
from copy import deepcopy

for i in range(100): print('')

def add_vectors(u, v):
    return [a + b for (a, b) in zip(u, v)]


a = [Q(1, METER), Q(1, METER), Q(1, METER)]
# a = [1,1,1]
b = [1,2,3]
c = add_vectors(a, b)

print(a)
print(b)
print(c)

