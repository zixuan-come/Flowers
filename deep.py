import copy

a = [1, 2, [3, 4]]
b = copy.copy(a)
b[0] = 99
print(a)  # 第一个打印
b[2][0] = 888
print(a)  # 第二个打印