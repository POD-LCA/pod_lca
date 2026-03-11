from pod_lca.units import METER, Quantity
from copy import deepcopy

for i in range(100): print('')

m = Quantity(10, METER)
a = deepcopy(m)

# class Tomas:

#     def __init__(self):
#         self.name = 'tomas'
#         self.age = 45
        
#     def __deepcopy__(self, memo):
#         cls = self.__class__
#         new_obj = cls.__new__(cls)
#         memo[id(self)] = new_obj
#         for k, v in self.__dict__.items():
#             setattr(new_obj, k, deepcopy(v, memo))
#         return new_obj

# t = Tomas()
# m = t
# m.name = 'mendez'

# print(t.name)
# print(m.name)



# # class MyObject:
# #     def __init__(self, name, data_list):
# #         self.name = name
# #         self.data_list = data_list  # A mutable object (like a list)

# #     def __deepcopy__(self, memo):
# #         print('tomas')
# #         # 1. Create a new instance without calling __init__ (optional)
# #         # Or, just create a new instance normally:
# #         new_obj = MyObject(self.name, deepcopy(self.data_list, memo))
        
# #         # 2. Add the new object to the memo dictionary to handle references
# #         memo[id(self)] = new_obj
        
# #         return new_obj
    

# # obj1 = MyObject("parent", [1, 2, 3])
# # obj2 = deepcopy(obj1)
# # obj2.data_list.append(4)

# # print(obj1.data_list) 
# # print(obj2.data_list) 

