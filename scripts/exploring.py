import json
import os

import pod_lca

for i in range(50): print('')




main = os.path.join(pod_lca.DATA, 'Ethan_Concrete_Mix')

# # Flows - - - - - -

# folder = os.path.join(main, 'flows')
# file = '0a2e68db-e3d3-406f-8347-9aab9793db55.json'

# filepath = os.path.join(folder, file)

# with open(filepath, 'r') as fp:
#     data = json.load(fp)

# for k in data:
#     print(k, data[k])
#     print('')



# processes - - - - 

folder = os.path.join(main, 'processes')
file = '0a0cd095-925f-367c-a0d8-57e82fe24916.json'

filepath = os.path.join(folder, file)

with open(filepath, 'r') as fp:
    data = json.load(fp)

for k in data:
    print(k)
    print('')

data = data['exchanges']
for k in data:
    print(k)
    print('')




# product systems - - - - 

# folder = os.path.join(main,'product_systems')
# file = 'c66b5fa6-e289-4b5e-8fe4-a088e2cc2201.json'
# filepath = os.path.join(folder, file)

# with open(filepath, 'r') as fp:
#     data = json.load(fp)

# # for k in data:
# #     print(k)
# #     print('')

# i = 2288
# data = data['processes']
# for k in data[i]:
#     print(k, data[i][k])
#     print('')

# data = data['processes']
# print(type(data))
# for i in data:
#     print(type(data[i]))
#     print('')